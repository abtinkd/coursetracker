from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.contrib.auth.models import User
from django.utils import timezone
from courses.models import Course
from courses.tests import get_choice
from django import forms
from courseperformance.forms import CourseDateRangeForm


class CourseRangeFormTestCase(TestCase):

    def setUp(self):
        self.user1, self.user2 = User.objects.create(username="test1", password="testtest"), \
                                 User.objects.create(username="test2", password="testtest")
        self.client = Client()
        self.client.force_login(self.user1)
        teardown_test_environment()
        setup_test_environment()

        self.course, self.other_course = Course.objects.create(name="Math", hours=5, user=self.user1),\
                                         Course.objects.create(name="Science", hours=1, user=self.user2)

    def test_display(self):
        """Make sure the user can see their own Courses."""
        self.assertTrue(get_choice(self.course, CourseDateRangeForm))

    def test_hidden(self):
        """Make sure we can't see the other user's Course."""
        self.assertFalse(get_choice(self.other_course, CourseDateRangeForm, user=self.user1))

    # TODO make tests for courses made outside of interval

# TODO later view test
