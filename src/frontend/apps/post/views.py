from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def index(request):
    pass

def listNews(request):
    posts = []
    wrappedPost = []
    allPosts = Post.objects.all()
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
    post = Post.objects.get(id=_id)
    return render(
        request, 'apps/post/detail.html', context={
            'post': post,
        }, content_type='text/html', status=200)
