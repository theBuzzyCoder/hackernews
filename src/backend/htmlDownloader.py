#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
import datetime
from requests import get


BASE_URL = "https://news.ycombinator.com"


def getCompleteUrl(urlPath: str) -> str:
    """Returns the complete url prefixed with BASE_URL"""
    return os.path.join(BASE_URL, urlPath) if urlPath else BASE_URL


def saveHtml(path: str, filename: str, html: str) -> None:
    """Saves html in specified filename in given path"""
    filepath = os.path.join(path, filename)
    with open(filepath, "w") as fileHandle:
        fileHandle.write(html)
    return None


def downloadHtml(url: str) -> str:
    httpResponse = get(url)
    if httpResponse.status_code == 200:
        html = httpResponse.text
    else:
        raise httpResponse.raise_for_status()
    return html


def getPaginationHyperlink(html: str) -> str:
    """Extracts hyperlink from more anchor tag"""
    moreLinkPattern = r'\<tr class="morespace".*?\<a\shref="(?P<hyperlink>.+?)"\sclass="morelink"'
    morelinkCompiledRegex = re.compile(moreLinkPattern, flags=re.IGNORECASE | re.DOTALL)
    matchedRegex = morelinkCompiledRegex.search(html)
    if matchedRegex:
        hyperlink = matchedRegex.group("hyperlink")
        return getCompleteUrl(hyperlink)
    else:
        return str()


def paginate(html: str) -> str:
    """Paginates accross different pages"""
    hyperlink = getPaginationHyperlink(html)
    return downloadHtml(hyperlink)


def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="Path where HTML file should be stored.")
    parser.add_argument("--filename", type=str, required=True, help="filename of HTML file.")
    parser.add_argument("--level", type=int, required=True, help="Number of times to paginate.")
    return parser.parse_args()


def getAppendedHtml(html: str, paginatedHtml: str) -> str:
    informationRowsPattern = r'(?P<start>.*?)(?P<informationRows>\<tr\s+class\=.athing.*\<\/tr\>\s+)(?P<end>\<tr\sclass=.morespace.*)'
    compiledRegex = re.compile(informationRowsPattern, flags=re.I | re.S)
    primaryInformation = compiledRegex.search(html).group("informationRows")

    # end is used from pagination html because the more link will point to the next page.
    # This would be helpful to crawl to next page
    (start, paginatedInformationRows, end) = compiledRegex.search(paginatedHtml).groups()
    html = start + primaryInformation + paginatedInformationRows + end
    return html


def startExecution():
    args = argumentParser()
    mailUrl = getCompleteUrl(None)
    print("Starting Download...", end="\n")
    html = downloadHtml(mailUrl)

    print("==========================================", end="\n")
    print("Downloaded Page 1", end="\n")
    for i in range(2, args.level + 1, 1):
        # This will overwrite previous html, and get new more link
        paginatedHtml = paginate(html)
        print("==========================================", end="\n")
        print(f"Downloaded Page {i}", end="\n")
        html = getAppendedHtml(html, paginatedHtml)
    (filename, extension) = os.path.splitext(args.filename)

    # TODO once testing is completed uncomment this link
    # filename = filename + datetime.datetime.strftime(datetime.datetime.now(), "_%Y_%b_%d_%H_%M_%S") + extension

    # TODO log the filepath in database so that the parser can pick the files from database.
    # And there is a logs of what file got downloaded when.
    saveHtml(args.path, filename, html)


if __name__ == '__main__':
    startExecution()
