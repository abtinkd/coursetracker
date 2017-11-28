from django.test import TestCase
from django.contrib.auth.models import User


class LogInTestCase(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'cs561Test'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_unauthorized_login(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': 'CS561TEST'}, follow=True)
        # should not be logged in now
        self.assertFalse(response.context['user'].is_authenticated)
