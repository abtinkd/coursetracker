from courses.models import Course
from courses.tests import get_choice
from courseperformance.forms import CourseDateRangeForm
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.contrib.auth.models import User
from django.utils import timezone
from timer.models import TimeInterval


class PerformanceFormTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test1", password="testtest")
        self.client = Client()
        self.client.force_login(self.user1)
        teardown_test_environment()
        setup_test_environment()

        self.course = Course.objects.create(name="Math", hours=5, user=self.user1)

    def test_display(self):
        """Make sure the user can see their own Courses."""
        self.assertTrue(get_choice(self.course, CourseDateRangeForm))

    def test_hidden(self):
        """Make sure we can't see another user's Course."""
        user2 = User.objects.create(username="test2", password="testtest")
        other_course = Course.objects.create(name="Science", hours=1, user=user2)

        self.assertFalse(get_choice(other_course, CourseDateRangeForm, user=self.user1))

    def test_deactivated_course(self):
        """Make sure that Courses deactivated before the start date are filtered out."""
        deactivated_course = Course.objects.create(name="deactived_course", hours=1, user=self.user1, activated=False,
                                                   deactivation_time=timezone.now() - timezone.timedelta(days=15))
        form = CourseDateRangeForm(data={'start_date': timezone.datetime.today() - timezone.timedelta(weeks=1),
                                         'end_date': timezone.datetime.today(), 'course': deactivated_course})
        self.assertFalse(form.is_valid())

    def test_not_started_course(self):
        """Make sure that Courses beginning after the date range are not allowed."""
        future_course = Course.objects.create(name="future_course", hours=1, user=self.user1)
        form = CourseDateRangeForm(data={'start_date': timezone.datetime.today() - timezone.timedelta(weeks=1),
                                         'end_date': timezone.datetime.today() - timezone.timedelta(days=1),
                                         'course': future_course})
        self.assertFalse(form.is_valid())


class PerformanceViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test", password="testtest", email='')
        self.course = Course.objects.create(name="Math", hours=5, user=self.user)
        for _ in range(2):
            TimeInterval.objects.create(course=self.course,
                                        start_time=timezone.now() - timezone.timedelta(seconds=2))

        self.client = Client()
        self.client.login(username='test', password='testtest')
        teardown_test_environment()
        setup_test_environment()

        # Two week date range
        session = self.client.session
        session['course_id'] = self.course.id
        session['start_date'] = (timezone.datetime.today() - timezone.timedelta(days=13)).strftime('%m-%d-%Y')
        session['end_date'] = timezone.datetime.today().strftime('%m-%d-%Y')
        session.save()

    def test_table(self):
        """Ensure that TimeIntervals are being properly displayed."""
        response = self.client.get('/courseperformance/display.html')
        self.assertEqual(len(response.context['table'].data.data), 2)
