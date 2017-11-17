from courses.forms import CreateCourseForm, EditCourseForm, DeleteCourseForm
from courses.models import Course
from timer.models import TimeInterval
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.utils import teardown_test_environment, setup_test_environment
from django.utils import timezone


class CourseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="testtest")
        Course.objects.create(name="Math", hours=5, user=self.user)
        Course.objects.create(name="Science", hours=1, user=self.user)


    def test_retrieval(self):
        """Ensure that we can retrieve a Course."""
        self.assertEqual("Math", Course.objects.filter(user=self.user).get(name="Math").__str__())

    def test_chinese(self):
        """Ensure that non-standard characters are supported."""
        Course.objects.create(name="好", hours=12, user=self.user)
        self.assertEqual("好", Course.objects.filter(user=self.user).get(name="好").__str__())

    # def test_negative(self):
    #    """Make sure that courses with negative hour goals cannot be created"""
    #    with self.assertRaises(db.utils.DataError)
    #        Course.objects.create(name="Shrek", hours=-1, user=self.user)

    #def test_long(self):  # TODO change database type from SQLite to something that supports char field length
    #    """Ensure that strings with length exceeding 50 characters are not supported."""
    #    with self.assertRaises(db.utils.DataError):
    #        Course.objects.create(name='l' * 51, user=self.user)


class CourseViewTestCase(TestCase):
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
        response = self.client.get('/courses/')
        self.assertTrue(self.course in response.context['table'].data)

    def test_hidden(self):
        """Make sure we can't see the other user's Course."""
        response = self.client.get('/courses/')
        self.assertFalse(self.other_course in response.context['table'].data)

    def test_delete(self):
        """Ensure deleted courses no longer show up."""
        self.course.delete()
        response = self.client.get('/courses/')
        self.assertFalse(self.course in response.context['table'].data)


class CreateFormTestCase(TestCase):
    def setUp(self):
        self.user1, self.user2 = User.objects.create(username="test1", password="testtest"), \
                                 User.objects.create(username="test2", password="testtest")

    def test_validation(self):
        """Make sure normal insertion works."""
        form = CreateCourseForm(data={'name': 'Math', 'hours': 5}, user=self.user1)
        self.assertTrue(form.is_valid())

        course = form.save(commit=True)
        self.assertEqual(Course.objects.filter(user=self.user1).get(name=course.name).name, 'Math')

    def test_duplicate(self):
        """Ensure that duplicate courses are not saved, but separate users can create identically-named courses."""
        # Normal creation
        form = CreateCourseForm(data={'name': 'Science', 'hours': 5}, user=self.user1)
        self.assertTrue(form.is_valid())
        form.save(commit=True)

        # Duplicate for user1
        form = CreateCourseForm(data={'name': 'Science', 'hours': 5}, user=self.user1)
        self.assertFalse(form.is_valid())

        # Normal creation
        form = CreateCourseForm(data={'name': 'Science', 'hours': 5}, user=self.user2)
        self.assertTrue(form.is_valid())  # can't add the same course again for the same user
        form.save(commit=True)
        self.assertEqual(Course.objects.filter(user=self.user2).get(name='Science').name, 'Science')

    def test_hidden(self):
        """Make sure that users can't see other users' data."""
        form = CreateCourseForm(data={'name': 'Science', 'hours': 5}, user=self.user1)
        form.save(commit=True)
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.filter(user=self.user2).get(name='Science')


class EditFormTestCase(TestCase):
    def setUp(self):
        self.user1, self.user2 = User.objects.create(username="test1", password="testtest"), \
                                 User.objects.create(username="test2", password="testtest")
        self.course, self.other_course = Course.objects.create(name="Math", hours=12, user=self.user1), \
                                         Course.objects.create(name="Science", hours=12, user=self.user2)

    def test_modify(self):
        """Make sure we can modify existing Courses using the edit form."""
        self.assertEqual(Course.objects.get(name='Math').name, 'Math')
        self.assertEqual(Course.objects.get(name='Math').hours, 12)

        # Do the modification
        form = EditCourseForm(data={'course': 1, 'name': 'htaM', 'hours': 21, 'activated': True}, user=self.user1)
        self.assertTrue(form.is_valid())
        form.save(commit=True)

        self.assertTrue(Course.objects.get(name='htaM').name)
        self.assertEqual(Course.objects.get(name='htaM').hours, 21)

    def test_modify_same_name(self):
        """Make sure we can modify existing Courses and enter their current name."""
        self.assertEqual(Course.objects.get(name='Math').hours, 12)

        # Do the modification
        form = EditCourseForm(data={'course': 1, 'name': 'Math', 'hours': 21, 'activated': True}, user=self.user1)
        self.assertTrue(form.is_valid())
        form.save(commit=True)

        self.assertEqual(Course.objects.get(name='Math').hours, 21)

    def test_modify_duplicate(self):
        """Make sure we can't name another Course to the name of an existing Course."""
        Course.objects.create(name='Science', hours=12, user=self.user1)
        form = EditCourseForm(data={'course': 1, 'name': 'Science', 'hours': 12, 'activated': True}, user=self.user1)
        self.assertFalse(form.is_valid())

    def test_deactivate(self):
        """Make sure we can deactivate existing Courses using the edit form."""
        # From activated...
        self.assertTrue(self.course.activated)
        form = EditCourseForm(data={'course': 1, 'hours': 15, 'activated': False}, user=self.user1)
        self.assertTrue(form.is_valid())
        form.save(commit=True)

        # Make sure it's deactivated, has a deactivation time, and the hours didn't change
        self.assertFalse(Course.objects.get(name='Math').activated)
        self.assertNotEqual(Course.objects.get(name='Math').deactivation_time, None)
        self.assertEqual(Course.objects.get(name='Math').hours, 12)

        # Make sure we can't reactivate
        form = EditCourseForm(user=self.user1)  # update form
        self.assertFalse(Course.objects.get(name='Math') in form.fields['course'].queryset)

    def test_hidden(self):
        """Make sure that users can't see other users' data."""
        form = EditCourseForm(user=self.user1)
        self.assertFalse(self.other_course in form.fields['course'].queryset)


class DeleteFormTestCase(TestCase):
    def setUp(self):
        self.user1, self.user2 = User.objects.create(username="test1", password="testtest"), \
                                 User.objects.create(username="test2", password="testtest")
        self.course, self.other_course = Course.objects.create(name="Math", hours=12, user=self.user1), \
                                         Course.objects.create(name="Science", hours=12, user=self.user2)
        self.search_time = timezone.now()  # mark start time of TimeInterval for later querying
        TimeInterval.objects.create(course=self.course, start_time=self.search_time)

    def test_delete(self):
        """Make sure that Courses and their corresponding TimeIntervals are properly deleted."""
        # Make sure the Course and its TimeIntervals exist
        self.assertEqual(Course.objects.filter(user=self.user1).get(name='Math').name, 'Math')
        self.assertEqual(TimeInterval.objects.get(start_time=self.search_time).course.name, 'Math')

        # Delete the Course
        form = DeleteCourseForm(data={'course': 1, 'hours': 12, 'activated': True}, user=self.user1)
        self.assertTrue(form.is_valid())
        form.delete()

        # Make sure the Course and TimeIntervals were deleted
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(name='Math')
        with self.assertRaises(TimeInterval.DoesNotExist):
            TimeInterval.objects.get(start_time=self.search_time)

    def test_hidden(self):
        """Make sure that users can't see other users' data."""
        form = DeleteCourseForm(user=self.user1)
        self.assertFalse(self.other_course in form.fields['course'].queryset)
