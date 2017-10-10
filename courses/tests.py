from courses.models import Course
from django.test import TestCase, Client
from django import db


class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(name="Math")
        Course.objects.create(name="Science")

    def test_retrieval(self):
        """Ensure that we can retrieve a course."""
        self.assertEqual("Math", Course.objects.get(name="Math").__str__())

    def test_duplicate(self):
        """Ensure that duplicate courses are not saved."""
        with self.assertRaises(db.utils.IntegrityError):
            Course.objects.create(name="Science")

    def test_chinese(self):
        """Ensure that non-standard characters are supported."""
        Course.objects.create(name="好")
        self.assertEqual("好", Course.objects.get(name="好").__str__())

    def test_long(self):
        """Ensure that strings with length exceeding 50 characters are not supported."""
        Course.objects.create(name='l'*51)
        print(Course.objects.order_by('name'))


# Verify that no courses are being displayed

# Send a request to create "Math" course
# Send a request to create a course with non-ascii characters (hanzi)
# Send a request to create a course whose name is longer than 50 characters
# Send a request to create a course which already exists

# Verify that only one course is being displayed
