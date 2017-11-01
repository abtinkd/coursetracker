import datetime
from courses.models import Course
from timer.models import TimeInterval
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.utils import timezone   


class HistoryViewTestCase(TestCase):  # TODO expand
    def setUp(self):
        # For testing basic functionality
        self.default_user = User.objects.create(username="test", password="testtest")
        self.client = Client()
        self.client.force_login(self.default_user)
        teardown_test_environment()
        setup_test_environment()
        self.course1, self.course2 = Course.objects.create(name="Math", hours=5, user=self.default_user),\
                                     Course.objects.create(name="Science", hours=2, user=self.default_user)

        for _ in range(2):  # so we can test summation is working
            TimeInterval.objects.create(course=self.course1, start_time=timezone.now() - datetime.timedelta(seconds=2))

        # For testing discretion over users displayed
        self.other_user = User.objects.create(username="other", password="testtest")
        self.other_course = Course.objects.create(name="Other Course", hours=5, user=self.other_user)
        TimeInterval.objects.create(course=self.other_course, start_time=timezone.now() - datetime.timedelta(seconds=2))

    def test_summation(self):
        """Ensure that TimeIntervals are being properly summed."""
        response = self.client.get('/history/')
        self.assertEqual(round(response.context['tallies'][0][1] * 3600), 4)  # x3600 to convert hours -> seconds

    def test_non_studied(self):
        """Make sure activated courses which had no TimeIntervals entered are still displayed as 0."""
        response = self.client.get('/history/')
        self.assertTrue((self.course2, 0) in response.context['tallies'])

    def test_hide_other_user(self):
        """Make sure we can't access the other user's TimeInterval from our data."""
        response = self.client.get('/history/')
        self.assertFalse(any([course[0] == self.other_course for course in response.context['tallies']]))

# TODO test form - make sure start can't be after end, make sure same-day works, make sure normal works
