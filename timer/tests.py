from courses.models import Course
from timer.models import TimeInterval
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


class TimeTestCase(TestCase):
    def setUp(self):
        self.default_user = User.objects.create(username="test", password="testtest")
        self.course = Course.objects.create(name="Math", hours=5, user=self.default_user)

    def test_retrieval(self):
        """Ensure that we can retrieve a TimeInterval."""
        TimeInterval.objects.create(course=self.course, start_time=timezone.now())
        self.assertEqual("Math", TimeInterval.objects.get(course=self.course).course.name)