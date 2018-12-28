from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


# class Avatar(models.Model):
#     image = models.ImageField()


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=datetime.now())


