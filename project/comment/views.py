from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from comment.models import *


def comments_by_user_id(request, user_id):
    try:
        comments = Comment.objects.filter(author_id=user_id)
    except Comment.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    return render(request, 'comment/comments_list.html', {"posts": comments})


def comment_by_id(request, comment_id):
    try:
        comment = Comment.objects.filter(id=comment_id)[0]
    except Comment.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'comment/comments_list.html', {"posts": list(comment)})


def comments_list(request):
    comments = Comment.objects.all()[:20]
    return render(request, 'comment/comments_list.html', {"posts": comments})

