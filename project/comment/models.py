from django.db import models
from django.utils import timezone
from blog.models import Post
from polls.models import Poll


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(db_index=True,
                                        default=timezone.now)

    post = models.ForeignKey(Post, related_name='comment')
    poll = models.ForeignKey(Poll, related_name='comment')

    def __str__(self):
        return 'comment to' + str(self.post)

