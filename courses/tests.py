from courses.forms import CourseForm, EditCourseForm
from courses.models import Course
from timer.models import TimeInterval
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


class CourseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="testtest")
        Course.objects.create(name="Math", hours=5, user=self.user)
        Course.objects.create(name="Science", hours=1, user=self.user)

    def test_retrieval(self):
        """Ensure that we can retrieve a Course."""
        self.assertEqual("Math (5)", Course.objects.filter(user=self.user).get(name="Math").__str__())

    def test_chinese(self):
        """Ensure that non-standard characters are supported."""
        Course.objects.create(name="好", user=self.user)
        self.assertEqual("好 (12)", Course.objects.filter(user=self.user).get(name="好").__str__())

    # def test_negative(self):
    #    """Make sure that courses with negative hour goals cannot be created"""
    #    with self.assertRaises(db.utils.DataError)
    #        Course.objects.create(name="Shrek", hours=-1, user=self.user)

    #def test_long(self):  # TODO change database type from SQLite to something that supports char field length
    #    """Ensure that strings with length exceeding 50 characters are not supported."""
    #    with self.assertRaises(db.utils.DataError):  # TODO check error is correct
    #        Course.objects.create(name='l' * 51, user=self.user)


class ModelFormTests(TestCase):
    def setUp(self):
        self.user1, self.user2 = User.objects.create(username="test1", password="testtest"), \
                                 User.objects.create(username="test2", password="testtest")

    def test_validation(self):
        """Make sure normal insertion works."""
        form = CourseForm(data={'name': 'Math', 'hours': 5})
        self.assertTrue(form.is_valid(self.user1))

        course = form.save(user=self.user1, commit=True)
        self.assertEqual(Course.objects.filter(user=self.user1).get(name=course.name).name, 'Math')

    def test_duplicate(self):
        """Ensure that duplicate courses are not saved, but separate users can create identically-named courses."""
        form = CourseForm(data={'name': 'Science', 'hours': 5})
        self.assertTrue(form.is_valid(self.user1))
        form.save(user=self.user1, commit=True)
        self.assertFalse(form.is_valid(self.user1))

        form = CourseForm(data={'name': 'Science', 'hours': 5})
        self.assertTrue(form.is_valid(self.user2))  # can't add the same course again for the same user
        form.save(user=self.user2, commit=True)
        self.assertEqual(Course.objects.filter(user=self.user2).get(name='Science').name, 'Science')

    def test_hidden(self):
        """Make sure that users can't see other users' data."""
        form = CourseForm(data={'name': 'Science', 'hours': 5})
        form.save(user=self.user1, commit=True)
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.filter(user=self.user2).get(name='Science')


class EditFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="testtest")
        self.course = Course.objects.create(name="Math", user=self.user)
        self.search_time = timezone.now()  # mark start time of TimeInterval for later querying
        TimeInterval.objects.create(course=self.course, start_time=self.search_time)

    def test_modify(self):
        """Make sure we can modify existing Courses using the edit form."""
        self.assertEqual(self.course.name, 'Math')
        self.assertEqual(self.course.hours, 12)

        # Do the modification
        form = EditCourseForm(data={'edit_course': 1, 'name': 'htaM', 'hours': 21, 'activated': True})
        self.assertTrue(form.is_valid(self.user))
        form.save(user=self.user, commit=True)

        self.assertTrue(Course.objects.get(name='htaM').name)  # assert this works
        self.assertEqual(Course.objects.get(name='htaM').hours, 21)

    def test_deactivate(self):
        """Make sure we can deactivate existing Courses using the edit form."""
        # From activated...
        self.assertTrue(self.course.activated)
        form = EditCourseForm(data={'edit_course': 1, 'hours': 12, 'activated': False})
        self.assertTrue(form.is_valid(self.user))
        form.save(user=self.user, commit=True)

        # To deactivated!
        self.assertFalse(Course.objects.get(name='Math').activated)

    def test_delete(self):
        """Make sure that Courses and their corresponding TimeIntervals are properly deleted."""
        # Make sure the Course and its TimeIntervals exist
        self.assertEqual(Course.objects.filter(user=self.user).get(name='Math').name, 'Math')
        self.assertEqual(TimeInterval.objects.get(start_time=self.search_time).course.name, 'Math')

        # Delete the Course
        form = EditCourseForm(data={'edit_course': 1, 'hours': 12, 'activated': True})
        self.assertTrue(form.is_valid(self.user))
        form.delete()

        # Make sure the Course and TimeIntervals were deleted
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(name='Math')
        with self.assertRaises(TimeInterval.DoesNotExist):
            TimeInterval.objects.get(start_time=self.search_time)
