import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from polls.models import *


def polls_by_user_id(request, user_id):
    polls_objects = Poll.objects.filter(author_id=user_id)
    polls = {}
    for poll_obj in polls_objects:
        choices = poll_obj.choice_set.all()
        polls.update({poll_obj: choices})

    return render(request, 'polls/polls_list.html', {"polls": polls})


def polls_list(request):
    polls_objects = Poll.objects.all()[:10]
    polls = {}
    for poll_obj in polls_objects:
        choices = poll_obj.choice_set.all()
        polls.update({poll_obj: choices})

    return render(request, 'polls/polls_list.html', {"polls": polls})


def get_choice_by_id(request, choice_id):
    try:
        choice = Choice.objects.get(id=choice_id)
    except Choice.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'polls/choice.html', {'choice': choice})


def current_datetime(request):
    print("Request -> ", request)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</html></body>" % now
    return HttpResponse(html)



