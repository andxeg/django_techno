import os, sys

proj_path = "/home/andrew/TECHNOSPHERE/python/env/django_project/project/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

import django
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment, Category
from polls.models import Poll, Choice
import datetime
from  random import randint

#Можно запрашивать из базы не содержимое объектов
# а только id объектов

#!!!Вопрос. Можно ли накопить queryset и только в самом конце отослать запрос в БАЗУ

#bulk_create
#в цикле к БД обращаться нельзя

#GENERATE POLLS IN DB
        

#GENERATE CATEGORIES

def init_db(argv):
    #CREATE_POLLS

    #CREATE_USERS


if __name__=="__main__":
    init_db(sys.argv[0:])


