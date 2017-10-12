from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hours = models.PositiveSmallIntegerField(default=12)

    def __str__(self):
        return '{} ({})'.format(self.name, self.hours)
