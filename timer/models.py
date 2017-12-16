from django.db import models
from courses.models import Course


class TimeInterval(models.Model):
    """Create a time interval showing when the user worked on a course."""
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)  # the course being worked on
    start_time = models.DateTimeField()  # when we first see it
    end_time = models.DateTimeField(auto_now_add=True)  # defaults to save time

    def __str__(self):
        return "{}: {} to {}".format(self.course, self.start_time, self.end_time)
