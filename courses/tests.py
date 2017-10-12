from courses.models import Course
from django.test import TestCase
from django import db


class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(name="Math", hours=5)
        Course.objects.create(name="Science", hours=1)

    def test_retrieval(self):
        """Ensure that we can retrieve a course."""
        self.assertEqual("Math (5)", Course.objects.get(name="Math").__str__())

    def test_duplicate(self):
        """Ensure that duplicate courses are not saved."""
        with self.assertRaises(db.utils.IntegrityError):
            Course.objects.create(name="Science")

    def test_negative(self):
        """Make sure that courses with negative hour goals cannot be created"""
        Course.objects.create(name="Shrek", hours=-1)

    def test_chinese(self):
        """Ensure that non-standard characters are supported."""
        Course.objects.create(name="好")
        self.assertEqual("好 (12)", Course.objects.get(name="好").__str__())

    #def test_long(self):  # TODO change database type from SQLite to something that supports char field length
    #    """Ensure that strings with length exceeding 50 characters are not supported."""
    #    with self.assertRaises(db.utils.DatabaseError):  # TODO check error is correct
    #        Course.objects.create(name='l' * 51)
