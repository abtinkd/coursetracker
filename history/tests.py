from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.utils import timezone
from courses.models import Course
from history.forms import DateRangeForm
from timer.models import TimeInterval


class DateRangeViewTestCase(TestCase):
    def setUp(self):
        self.default_user = User.objects.create_superuser(username="test", password="testtest", email='')
        self.client = Client()
        self.client.login(username='test', password='testtest')
        teardown_test_environment()
        setup_test_environment()

    def test_presets(self):  # TODO ensure works with timezones
        """Ensure the button presets in the index view set the proper dates."""
        def get_date_range(client):
            """Retrieves the timedelta (in days) of start_date and end_date from client.session."""
            start_date, end_date = client.session.__getitem__('start_date'), client.session.__getitem__('end_date')
            start_date, end_date = timezone.datetime.strptime(start_date, '%m-%d-%Y'), \
                                   timezone.datetime.strptime(end_date, '%m-%d-%Y')
            return (end_date - start_date).days

        # Each key corresponds to how many days it should represent
        today = timezone.datetime.today()
        for key, val in (('year', 365), ('month', (today - (today - relativedelta(months=+1))).days),
                         ('week', 7), ('current', 7)):
            self.client.post('/history/', {key: ['']})
            self.assertEquals(get_date_range(self.client), val)


class HistoryViewTestCase(TestCase):
    def setUp(self):
        self.default_user = User.objects.create_superuser(username="test", password="testtest", email='')
        self.course1, self.course2 = Course.objects.create(name="Math", hours=5, user=self.default_user), \
                                     Course.objects.create(name="Science", hours=2, user=self.default_user)

        for _ in range(2):  # so we can test summation is working
            TimeInterval.objects.create(course=self.course1,
                                        start_time=timezone.now() - timezone.timedelta(seconds=2))

        # Out-of-date-range TimeInterval
        TimeInterval.objects.create(course=self.course2, start_time=timezone.now() - timezone.timedelta(weeks=4),
                                    end_time=timezone.now() - timezone.timedelta(weeks=3))

        # For testing discretion over users displayed
        self.other_user = User.objects.create(username="other", password="testtest")
        self.other_course = Course.objects.create(name="Other Course", hours=5, user=self.other_user)
        TimeInterval.objects.create(course=self.other_course, start_time=timezone.now() - timezone.timedelta(seconds=2))

        self.client = Client()
        self.client.login(username='test', password='testtest')
        teardown_test_environment()
        setup_test_environment()

        # Two week date range
        session = self.client.session
        session['start_date'] = (timezone.datetime.today() - timezone.timedelta(days=13)).strftime('%m-%d-%Y')
        session['end_date'] = timezone.datetime.today().strftime('%m-%d-%Y')
        session.save()

    def test_summation(self):
        """Ensure that TimeIntervals are being properly summed."""
        response = self.client.get('/history/display.html')
        courses = response.context['courses']
        course = next(course for course in response.context['courses'] if course == self.course1)
        self.assertAlmostEqual(course.time_spent * 3600, 4, places=1)  # x3600 to convert hours -> seconds

    def test_non_studied(self):
        """Make sure activated Courses without TimeIntervals have their time spent marked 0."""
        response = self.client.get('/history/display.html')
        self.assertTrue(self.course2 in response.context['courses'])

    def test_hide_other_user(self):
        """Make sure we can't access the other user's TimeInterval from our data."""
        response = self.client.get('/history/display.html')
        with self.assertRaises(StopIteration):
            next(course for course in response.context['courses'] if course == self.other_course)

    def test_bounds(self):
        """Make sure that Courses which were not active during any part of the date range are not shown."""
        early_course = Course.objects.create(name="Early", hours=1, user=self.default_user, activated=False,
                                             deactivation_time=timezone.now() - timezone.timedelta(days=15))
        response = self.client.get('/history/display.html')
        self.assertFalse(early_course in response.context['courses'])

        # Make it so today is outside of the date range
        session = self.client.session
        session['end_date'] = (timezone.datetime.today() - timezone.timedelta(days=1)).strftime('%m-%d-%Y')
        session.save()
        late_course = Course.objects.create(name="Late", hours=1, user=self.default_user)

        response = self.client.get('/history/display.html')
        self.assertFalse(late_course in response.context['courses'])

    def test_hours(self):
        """Ensure that total hourly goals scale with the date range."""
        session = self.client.session
        session['start_date'] = (timezone.datetime.today()).strftime('%m-%d-%Y')
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(weeks=2)).strftime('%m-%d-%Y')
        session.save()

        response = self.client.get('/history/display.html')
        course = next(course for course in response.context['courses'] if course == self.course1)
        self.assertAlmostEqual(course.total_target_hours, course.hours * 2, places=2)

    def test_deactivation_hours(self):
        """Make sure that the total hour goal scales with how many days the Course was active during the date range."""
        half_active_course = Course.objects.create(name="Half", hours=10, user=self.default_user, activated=False,
                                                   deactivation_time=timezone.now() + timezone.timedelta(microseconds=1))

        session = self.client.session
        session['start_date'] = (timezone.datetime.today()).strftime('%m-%d-%Y')
        session['end_date'] = (timezone.datetime.today() + timezone.timedelta(weeks=1)).strftime('%m-%d-%Y')
        session.save()

        response = self.client.get('/history/display.html')
        course = next(course for course in response.context['courses'] if course == half_active_course)
        self.assertEqual(course.total_target_hours, half_active_course.hours / 7)


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
