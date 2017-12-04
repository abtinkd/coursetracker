from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone as tz
from timezone_field import TimeZoneField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #timezone = TimeZoneField(default=tz.get_current_timezone())  TODO implement


def get_timezone(user):
    return UserProfile.objects.get(user=user).timezone