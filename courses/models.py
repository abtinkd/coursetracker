from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=25)
    hours = models.PositiveSmallIntegerField()
    user = models.ForeignKey(to=User)
    activated = models.BooleanField(default=True,
                                    help_text='Deactivated courses still appear in history, but cannot be reactivated.')

    creation_time = models.DateTimeField(auto_now_add=True)
    deactivation_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
