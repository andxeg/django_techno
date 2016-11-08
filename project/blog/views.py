from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from blog.models import *


def posts_by_user_id(request, user_id):
    try:
        posts = Post.objects.filter(author_id=user_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'blog/posts_list.html', {"posts": posts})


def posts_list(request):
    posts = Post.objects.all()[:20]
    return render(request, 'blog/posts_list.html', {"posts": posts})


def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories_list.html', {"categories": categories})


# def category_by_id(request, category_id):
#     try:
#         category = Category.objects.filter(id=category_id)[0]
#     except Category.DoesNotExist:
#         return HttpResponseNotFound('<h1>Page not found</h1>')
#     return render(request, 'blog/category_post_list.html', {"categories": category})

