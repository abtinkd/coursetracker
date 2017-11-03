from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.utils import timezone

from courses.models import Course
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
        # Two week interval
        session['start_date'] = (timezone.datetime.today() - timezone.timedelta(days=13)).strftime('%m-%d-%Y')
        # Add one to end_date to mirror what happens in is_valid - make sure we can see what was entered *on* end_date
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(days=1)).strftime('%m-%d-%Y')
        session.save()

        self.course1, self.course2 = Course.objects.create(name="Math", hours=5, user=self.default_user),\
                                     Course.objects.create(name="Science", hours=2, user=self.default_user)

        for _ in range(2):  # so we can test summation is working
            TimeInterval.objects.create(course=self.course1, start_time=timezone.now() - timezone.timedelta(seconds=2))

        # Out-of-date-range TimeInterval
        TimeInterval.objects.create(course=self.course2, start_time=timezone.datetime.now() - timezone.timedelta(weeks=2),
                                    end_time=timezone.now() - timezone.timedelta(hours=1))

        # For testing discretion over users displayed
        self.other_user = User.objects.create(username="other", password="testtest")
        self.other_course = Course.objects.create(name="Other Course", hours=5, user=self.other_user)
        TimeInterval.objects.create(course=self.other_course, start_time=timezone.now() - timezone.timedelta(seconds=2))

    def test_summation(self):
        """Ensure that TimeIntervals are being properly summed."""
        response = self.client.get('/history/display.html')
        tally = next(tally for tally in response.context['tallies'] if tally[0] == self.course1)
        self.assertEqual(round(tally[1] * 3600), 4)  # x3600 to convert hours -> seconds

    def test_non_studied(self):
        """Make sure activated courses which had no TimeIntervals entered during the given date range are 0."""
        response = self.client.get('/history/display.html')
        self.assertTrue((self.course2, 0) in response.context['tallies'])

    def test_hide_other_user(self):
        """Make sure we can't access the other user's TimeInterval from our data."""
        response = self.client.get('/history/display.html')
        self.assertFalse(any([course[0] == self.other_course for course in response.context['tallies']]))

    def test_history_bounds(self):
        """Make sure that Courses which were not active during any part of the date range are not shown."""
        early_course = Course.objects.create(name="Early", hours=1, user=self.default_user, activated=False,
                                             deactivation_time=timezone.datetime.now() - timezone.timedelta(days=15))
        response = self.client.get('/history/display.html')
        self.assertFalse(early_course in response.context['tallies'])

        # Make it so today is outside of the date range
        session = self.client.session
        session['end_date'] = (timezone.datetime.today() - timezone.timedelta(days=1)).strftime('%m-%d-%Y')
        session.save()
        late_course = Course.objects.create(name="Late", hours=1, user=self.default_user)

        response = self.client.get('/history/display.html')
        self.assertFalse(late_course in response.context['tallies'])

    def test_whole_interval_hours_scaling(self):
        """Ensure that total hourly goals scale correctly when courses are active throughout the date range."""
        session = self.client.session
        session['start_date'] = (timezone.datetime.today()).strftime('%m-%d-%Y')
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(weeks=1)).strftime('%m-%d-%Y')
        session.save()

        response = self.client.get('/history/display.html')
        course = next(tally[0] for tally in response.context['tallies'] if tally[0] == self.course1)
        # Error range because creation time (probably) wasn't at 0h0m0s today
        self.assertTrue(self.course1.hours * .8 <= course.total_target_hours <= self.course1.hours)

        # Extend another week
        session = self.client.session
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(weeks=2)).strftime('%m-%d-%Y')
        session.save()

        response = self.client.get('/history/display.html')
        course = next(tally[0] for tally in response.context['tallies'] if tally[0] == self.course1)
        self.assertTrue(self.course1.hours * 1.6 <= course.total_target_hours <= self.course1.hours * 2 )

    def test_deactivation_hours_scaling(self):
        """Make sure that the total hour goal scales with how long the Course was active during the date range."""
        half_active_course = Course.objects.create(name="Half", hours=10, user=self.default_user, activated=False,
                                                   deactivation_time=timezone.datetime.now() +
                                                                     timezone.timedelta(days=3, hours=12))

        session = self.client.session
        session['start_date'] = (timezone.datetime.today()).strftime('%m-%d-%Y')
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(weeks=1)).strftime('%m-%d-%Y')
        session.save()

        response = self.client.get('/history/display.html')
        self.assertTrue(half_active_course.hours * .5 * .8 <=
                        next(tally[0].total_target_hours for tally in response.context['tallies']
                             if tally[0] == half_active_course) <=
                        half_active_course.hours * .5 * 1.2)


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
