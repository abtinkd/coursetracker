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

    #def test_negative(self):
    #    """Make sure that courses with negative hour goals cannot be created"""
    #    with self.assertRaises(db.utils.DataError)
    #        Course.objects.create(name="Shrek", hours=-1)

    def test_chinese(self):
        """Ensure that non-standard characters are supported."""
        Course.objects.create(name="好")
        self.assertEqual("好 (12)", Course.objects.get(name="好").__str__())

    #def test_long(self):  # TODO change database type from SQLite to something that supports char field length
    #    """Ensure that strings with length exceeding 50 characters are not supported."""
    #    with self.assertRaises(db.utils.DataError):  # TODO check error is correct
    #        Course.objects.create(name='l' * 51)

    # TODO make sure users can only see their own data on pages


class ModelFormTests(unittest.TestCase):
    def test_validation(self):
        form_data = {'name': 'My Course', 'hours': 5}

        form = ContactForm(data=form_data)
        self.assert_(form.is_valid())
        self.assertEqual(form.instance.name, 'Test Name')

        form.save()

        self.assertEqual(Contact.objects.get(id=form.instance.id).name, 'Test Name')

    def test_duplicate(self):  # TODO make sure it checks across users
        """Ensure that duplicate courses are not saved."""
        with self.assertRaises(forms.ValidationError):
            Course.objects.create(name="Science")