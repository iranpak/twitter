from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


# class Avatar(models.Model):
#     image = models.ImageField()


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, default='Tweet')
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)


class Request(models.Model):
    ip_addr = models.CharField(max_length=24)
    browser = models.CharField(max_length=256)
    created_at = models.DateTimeField(timezone.now)
    unauthorized = models.BooleanField(default=False)

