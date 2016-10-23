import datetime
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    author = models.ForeignKey('auth.User')
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(db_index=True, default=timezone.now)

    def __str__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self. choice_text


class Answer(models.Model):
    choice = models.ForeignKey(Choice)
    author = models.ForeignKey('auth.User') 

    def __str__(self):
        return str(self.author) + '_' + str(self.choice)


