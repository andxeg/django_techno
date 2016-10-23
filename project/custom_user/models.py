from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    about = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)
