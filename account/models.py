from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    university = models.CharField(max_length=100, default='')
    interests = models.CharField(max_length=500, default='')
