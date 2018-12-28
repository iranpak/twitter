from django.contrib.auth.models import User
from django.db import models
from tw_auth.models import models as tw_models

# Create your models here.


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
