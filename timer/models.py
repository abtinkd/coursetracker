from django.db import models
from courses import Course


class TimeInterval(models.Model):
    """Create a time interval showing when the user worked on a course."""
    course = Course()  # the course being worked on
    start_time = models.DateTimeField(auto_now_add=True)  # defaults to creation time
    end_time = models.DateTimeField()

    def __str__(self):
        return "{}: {} to {}".format(self.course, self.start_time, self.end_time)
