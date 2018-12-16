import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db.models import Max
from .models import Post


def detail_view_not_found(request, _id):
    max_id = Post.objects.all().aggregate(Max("id"))
    return render(request, 'admin/404.html', context={
        'post_id': _id, "max_id": max_id["id__max"]
    }, content_type='text/html', status=404)


def listNews(request):
    posts = []
    wrappedPost = []
    allPosts = Post.objects.all().filter(is_deleted=0)
    for index, post in enumerate(allPosts, 1):
        wrappedPost.append(post)
        if index % 2 == 0:
            posts.append(wrappedPost)
            wrappedPost = []
    return render(
        request, 'apps/post/list.html', context={
            'allPosts': posts,
        }, content_type='text/html', status=200)


def getNews(request, _id):
    try:
        post = Post.objects.get(id=_id, is_deleted=0)
    except Post.DoesNotExist:
        return detail_view_not_found(request, _id)
    post.is_read = 1
    post.save()
    max_id = Post.objects.all().aggregate(Max("id"))
    return render(
        request, 'apps/post/detail.html', context={
            'post': post, "max_id": max_id["id__max"]
        }, content_type='text/html', status=200)


def deleteNews(request, _id):
    post = Post.objects.get(id=_id)
    post.is_deleted = 1
    post.save()
    return redirect('/')


def page(request, filepath):
    fullpath = os.path.join('/code/fileBucket', filepath)
    if os.path.exists(fullpath) and os.path.isfile(fullpath):
        with open(fullpath) as f:
            return HttpResponse(f.read())
    else:
        raise Http404('File not found!')
