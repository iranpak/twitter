from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TokenV1(models.Model):
    user_authentication = models.ForeignKey(User, on_delete=models.CASCADE)
    authentication_key = models.UUIDField()
    is_valid = models.BooleanField(default=True)

