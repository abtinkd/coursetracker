from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=50)  # TODO make unique for user
    hours = models.PositiveSmallIntegerField(default=12)
    user = models.ForeignKey(to=User, default=None)

    def __str__(self):
        return '{} ({})'.format(self.name, self.hours)
