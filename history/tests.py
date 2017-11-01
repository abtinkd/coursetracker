from courses.models import Course
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.utils import timezone
from history.forms import DateRangeForm
from timer.models import TimeInterval


class HistoryViewTestCase(TestCase):  # TODO fix RuntimeWarnings?
    def setUp(self):
        # For testing basic functionality
        self.default_user = User.objects.create_superuser(username="test", password="testtest", email='')
        self.client = Client()
        self.client.login(username='test', password='testtest')
        teardown_test_environment()
        setup_test_environment()
        session = self.client.session
        session['start_date'] = (timezone.datetime.today() - timezone.timedelta(weeks=1)).strftime('%m-%d-%Y')
        # Add one to end_date to mirror what happens in is_valid - make sure we can see what was entered *on* end_date
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(days=1)).strftime('%m-%d-%Y')
        session.save()

        self.course1, self.course2 = Course.objects.create(name="Math", hours=5, user=self.default_user),\
                                     Course.objects.create(name="Science", hours=2, user=self.default_user)

        for _ in range(2):  # so we can test summation is working
            TimeInterval.objects.create(course=self.course1, start_time=timezone.now() - timezone.timedelta(seconds=2))

        # Out-of-date-range TimeInterval
        TimeInterval.objects.create(course=self.course2, start_time=timezone.datetime.today() - timezone.timedelta(weeks=2),
                                    end_time=timezone.now() - timezone.timedelta(hours=1))

        # For testing discretion over users displayed
        self.other_user = User.objects.create(username="other", password="testtest")
        self.other_course = Course.objects.create(name="Other Course", hours=5, user=self.other_user)
        TimeInterval.objects.create(course=self.other_course, start_time=timezone.now() - timezone.timedelta(seconds=2))

        self.response = self.client.get('/history/display.html')

    def test_summation(self):
        """Ensure that TimeIntervals are being properly summed."""
        self.assertEqual(round(self.response.context['tallies'][0][1] * 3600), 4)  # x3600 to convert hours -> seconds

    def test_non_studied(self):
        """Make sure activated courses which had no TimeIntervals entered during the given date range are 0."""
        self.assertTrue((self.course2, 0) in self.response.context['tallies'])

    def test_hide_other_user(self):
        """Make sure we can't access the other user's TimeInterval from our data."""
        self.assertFalse(any([course[0] == self.other_course for course in self.response.context['tallies']]))


class DateRangeFormTestCase(TestCase):
    def test_normal(self):
        """Make sure the start date can be before the end date."""
        form = DateRangeForm(data={'start_date': timezone.datetime.today() - timezone.timedelta(weeks=1),
                                   'end_date': timezone.datetime.today()})
        self.assertTrue(form.is_valid())

    def test_same_day(self):
        """Make sure the start and end dates can be the same."""
        form = DateRangeForm(data={'start_date': timezone.datetime.today(), 'end_date': timezone.datetime.today()})
        self.assertTrue(form.is_valid())

    def test_invalid_start(self):
        """Make sure the start date can't be after the end date."""
        form = DateRangeForm(data={'start_date': timezone.datetime.today(),
                                   'end_date': timezone.datetime.today() - timezone.timedelta(weeks=1)})
        self.assertFalse(form.is_valid())
