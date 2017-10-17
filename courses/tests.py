from courses.forms import CourseForm
from courses.models import Course
from django.contrib.auth.models import User
from django.test import TestCase


class CourseTestCase(TestCase):
    def setUp(self):
        self.default_user = User.objects.create(username="test", password="testtest")
        Course.objects.create(name="Math", hours=5, user=self.default_user)
        Course.objects.create(name="Science", hours=1, user=self.default_user)

    def test_retrieval(self):
        """Ensure that we can retrieve a Course."""
        self.assertEqual("Math (5)", Course.objects.filter(user=self.default_user).get(name="Math").__str__())

    def test_chinese(self):
        """Ensure that non-standard characters are supported."""
        Course.objects.create(name="好", user=self.default_user)
        self.assertEqual("好 (12)", Course.objects.filter(user=self.default_user).get(name="好").__str__())

    # def test_negative(self):
    #    """Make sure that courses with negative hour goals cannot be created"""
    #    with self.assertRaises(db.utils.DataError)
    #        Course.objects.create(name="Shrek", hours=-1, user=self.default_user)

    #def test_long(self):  # TODO change database type from SQLite to something that supports char field length
    #    """Ensure that strings with length exceeding 50 characters are not supported."""
    #    with self.assertRaises(db.utils.DataError):  # TODO check error is correct
    #        Course.objects.create(name='l' * 51, user=self.default_user)


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
