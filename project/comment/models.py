from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_date = models.DateTimeField(db_index=True,
                                        default=timezone.now)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'comment to ' + str(self.content_object)

    class Meta:
        pass

# find connected object Post or Polls
# !!!FIRST METHOD
# from blog.models import Post
# from django.contrib.contenttypes.models import ContentType
# c = Comment.objects.get(title='Comment #1')
# co = ContentType.objects.get_for_model(Post)
# model = co.model_class()
# post = model.objects.get(id=c.object_id)

# !!!SECOND METHOD
# from django.contrib.contenttypes.models import ContentType
# c = Comment.objects.get(title='Comment #1')
# model = c.content_type.model_class()
# post = model.objects.get(id=c.object_id)

# !!!THIRD METHOD
# directly through db_id
# from django.contrib.contenttypes.models import ContentType
# c = Comment.objects.get(title='Comment #1')
# co = ContentType.objects.get(id=c.content_type_id)
# model = co.model_class()
# post = model.objects.get(id=c.object_id)


