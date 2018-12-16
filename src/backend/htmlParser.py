#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import pytz
import argparse
from datetime import timedelta, datetime
from bs4 import BeautifulSoup as bsoup4
from setup_django import setupDjango


RE_TIME = r'(?P<timedelta>\d+)\s*(?P<time_format>week|day|hour|minute|second)(?:s)?\s+ago'


def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="Path where HTML file should be stored.")
    parser.add_argument("--filename", type=str, required=True, help="filename of HTML file.")
    return parser.parse_args()


# Had too many drawbacks. Can't set values with proper data field types. Like duration for example.
# def getDatabaseConnection():
#     return MySQLdb.connect(db='hackernews', user='admin', password='admin', host='db', port=3306)
#
#
# def getCursor(connection=None, isDictCursor=False):
#     if not connection:
#         connection = getDatabaseConnection()
#     return MySQLdb.DictCursor(connection) if isDictCursor else connection.cursor()


def loadHtml(filepath: str, filename: str) -> str:
    html = ""
    fullFilePath = os.path.join(filepath, filename)
    if os.path.exists(fullFilePath) and os.path.isfile(fullFilePath):
        with open(fullFilePath, mode="r") as readHandle:
            html = readHandle.read()
    return html


def parse(path: str, filename: str):
    data_dict_list = list()
    timedeltaFilterer = re.compile(RE_TIME, flags=re.I)

    html = loadHtml(path, filename)
    if not html:
        print(f"File not found {path}/{filename}", end="\n")
        return

    soup = bsoup4(markup=html, features='html5lib')

    itemsTable = soup.find(name='table', class_='itemlist')
    subjectRows = itemsTable.find_all(name='tr', class_='athing')

    for subjectRow in subjectRows:
        data_dict = dict()

        # Get news url and subject from first <tr>
        anchor = subjectRow.find(name='a', class_='storylink')
        data_dict['hacker_news_url'] = anchor.attrs.get('href')
        data_dict['subject'] = anchor.text.strip()

        # Get upvote, comments and post age from the immediate next <tr>
        additionalInfoRow = subjectRow.next_sibling  # Getting next <tr>
        subtextCol = additionalInfoRow.find(name="td", class_='subtext')  # Getting <td> having actual information

        data_dict['upvotes'] = 0
        scoreSpan = subtextCol.find(name='span', class_='score')
        if scoreSpan:
            # Found an occurrence where there weren't any upvotes.
            # Hence added the condition to check if score span tag is present.
            upvotesFilterObject = filter(str.isnumeric, scoreSpan.text)
            data_dict['upvotes'] = int(''.join(upvotesFilterObject))

        timedeltaStr = subtextCol.find(name='span', class_='age').text.strip()
        age, ageFormat = timedeltaFilterer.search(timedeltaStr).group('timedelta', 'time_format')
        data_dict['post_age'] = timedelta(**{ageFormat + 's': int(age)})

        data_dict['comments'] = 0
        commentAnchorTag = subtextCol.find(name='a', text=re.compile(r'comment', flags=re.IGNORECASE))
        if commentAnchorTag:
            # Found an occurrence where comments where not present.
            data_dict['comments'] = int(''.join(filter(str.isnumeric, commentAnchorTag.text)))
        postObject = Post(**data_dict)
        try:
            postObject.save()
        except django.db.IntegrityError as e:
            postObject = Post.objects.get(subject=data_dict['subject'])
            postObject.__dict__.update(data_dict)
            postObject.save()


if __name__ == '__main__':
    setupDjango()
    from apps.post.models import Post
    args = argumentParser()

    print("Starting page data extraction now ...")
    parse(args.path, args.filename)
    print("Done!")
