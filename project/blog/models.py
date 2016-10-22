from django.db import models
from django.utils import timezone


class Category(models.Model):
    #index for select with ORDER BY
    headline = models.CharField(db_index=True, max_length=200)

    def __str__(self):
       return self.headline

    class Meta:
        ordering = ('headline',)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    categories = models.ManyToManyField(Category)
    #index for select with ORDER BY
    title = models.CharField(db_index=True, max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(db_index=True,
                                        default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(db_index=True,
            default=timezone.now)

    post = models.ForeignKey('Post')
    
    def __str__(self):
        return 'comment to' + str(self.post)


