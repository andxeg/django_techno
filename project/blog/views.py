from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from blog.models import *


def post_by_id(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # categories = list(post.categories.values_list('id', flat=True).all())
    categories = list(post.categories.all())
    print("Categories -> ", categories)
    
    return render(request, 'blog/posts_list.html', {"posts_and_categories": {post: categories}})


def posts_by_user_id(request, user_id):
    try:
        posts = Post.objects.filter(author_id=user_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    posts_and_categories = {}
    for post in posts:
        # categories = list(post.categories.values_list('id', flat=True).all())
        categories = list(post.categories.all())
        posts_and_categories.update({post: categories})

    return render(request, 'blog/posts_list.html', {"posts_and_categories": posts_and_categories})


def posts_list(request):
    posts = Post.objects.all()[:20]

    posts_and_categories = {}
    for post in posts:
        # categories = list(post.categories.values_list('id', flat=True).all())
        categories = list(post.categories.all())
        posts_and_categories.update({post: categories})

    return render(request, 'blog/posts_list.html', {"posts_and_categories": posts_and_categories})


def categories_list(request):
    categories = Category.objects.all()

    categories_posts = {}

    for category in categories:
        # TODO not effective
        posts = category.post_set.all()[:5]
        categories_posts.update({category: posts})

    return render(request, 'blog/categories_list.html', {"categories_posts": categories_posts})


def category_by_id(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    posts = category.post_set.all()
    return render(request, 'blog/category_full.html', {"category_posts": [category, posts]})

