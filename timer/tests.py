from courses.models import Course
from timer.forms import CourseSelectionForm
from timer.models import TimeInterval
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


class TimeIntervalTestCase(TestCase):  # TODO add viewtest for start_time
    def setUp(self):
        self.default_user = User.objects.create(username="test", password="testtest")
        self.course = Course.objects.create(name="Math", hours=5, user=self.default_user)

    def test_retrieval(self):
        """Ensure that we can retrieve a TimeInterval."""
        TimeInterval.objects.create(course=self.course, start_time=timezone.now())
        self.assertEqual("Math", TimeInterval.objects.get(course=self.course).course.name)


class CourseSelectionFormTestCase(TestCase):
    def setUp(self):
        self.user1, self.user2 = User.objects.create(username="test1", password="testtest"), \
                                 User.objects.create(username="test2", password="testtest")
        self.course1, self.course2 = Course.objects.create(name="Math", hours=12, user=self.user1),\
                                     Course.objects.create(name="Science", hours=12, user=self.user2)

    def test_retrieval(self):
        """Make sure the user's own Courses are displayed."""
        form = CourseSelectionForm(user=self.user1)
        self.assertTrue(self.course1 in form.fields['course'].queryset)

    def test_hidden(self):
        """Make sure we can't activate the timer for other users' Courses."""
        form = CourseSelectionForm(user=self.user1)
        self.assertFalse(self.course2 in form.fields['course'].queryset)
