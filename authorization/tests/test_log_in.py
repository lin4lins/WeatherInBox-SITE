from django.test import Client
from django.urls import reverse

from authorization.forms import LogInForm
from authorization.tests import LOGIN_VALID_DATA, CustomTestCase
from authorization.views.log_in_out import LogInView


class LogInViewViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.success_url = reverse('home')
        self.valid_data = LOGIN_VALID_DATA
        self.field_missing_data = {
             'password': 'testPassword99'
        }
        self.username_empty_data = {
            'username': '',
            'password': 'testPassword'
        }
        self.password_empty_data = {
            'username': 'testuser',
            'password': ''
        }
        self.invalid_credentials_data = {
            'username': 'testuser',
            'password': 'testPassword'
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, LogInView.template_name)
        self.assertIsInstance(response.context['form'], LogInForm)

    def test_post_valid_data(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_post_field_missing(self):
        response = self.client.post(self.url, self.field_missing_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('username', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('username'))

    def test_post_username_empty(self):
        response = self.client.post(self.url, self.username_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('username', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('username'))

    def test_post_password_empty(self):
        response = self.client.post(self.url, self.password_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('password', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('password'))

    def test_post_invalid_credentials(self):
        response = self.client.post(self.url, self.invalid_credentials_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('__all__', response.context['form'].errors.keys())
        self.assertIn('No active account found with the given credentials', response.context['form'].errors.get('__all__'))
