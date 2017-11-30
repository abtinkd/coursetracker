from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.contrib.auth.models import User
from django.utils import timezone
from courses.models import Course
from courses.tests import get_choice
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

    def test_deactivated_course(self):
        """Make sure that Course has not deactivate before selected date range."""
        deactivated_course = Course.objects.create(name="deactive_course", hours=1, user=self.user1, activated=False,
                                                   deactivation_time=timezone.now() - timezone.timedelta(days=15))
        form = CourseDateRangeForm(data={'start_date': timezone.datetime.today() - timezone.timedelta(weeks=1),
                                   'end_date': timezone.datetime.today(), 'course':    deactivated_course
                                         })
        self.assertFalse(form.is_valid())

    def test_not_started_course(self):
        """Make sure that Course has not started after selected date range."""
        not_started_course = Course.objects.create(name="not_started_course", hours=1, user=self.user1)
        form = CourseDateRangeForm(data={'start_date': timezone.datetime.today() - timezone.timedelta(days=1),
                                   'end_date': timezone.datetime.today()- timezone.timedelta(weeks=1), 'course': not_started_course
                                         })
        self.assertFalse(form.is_valid())


# TODO later view test
