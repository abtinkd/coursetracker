from courses.models import Course
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.utils import timezone
from timer.forms import CourseSelectionForm
from timer.models import TimeInterval
from tracker.helper import get_choice


class TimeIntervalTestCase(TestCase):
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


class TimerViewTestCase(TestCase):
    def setUp(self):
        self.default_user = User.objects.create_superuser(username="test", password="testtest", email='')
        self.course = Course.objects.create(name="Math", hours=5, user=self.default_user)

        self.client = Client()
        self.client.login(username='test', password='testtest')
        teardown_test_environment()
        setup_test_environment()

    def test_normal(self):
        """Ensure TimeIntervals are created properly."""
        response = self.client.get('/history/display.html')
        course = next(course for course in response.context['courses'] if course == self.course)
        self.assertAlmostEqual(course.time_spent * 3600, 4, places=1)  # x3600 to convert hours -> seconds

    def test_no_duplicate_submissions(self):
        """Ensure that the same form cannot be submitted multiple times by clicking very quickly."""
        session = self.client.session
        session['course_id'] = get_choice(self.course, CourseSelectionForm)
        session.save()
        response = self.client.get('/history/display.html')
        self.assertEqual(len(response.context['table'].data.data), 2)
