from django.test import Client
from django.urls import reverse

from authorization.tests import (LOGIN_VALID_DATA2, USER_2_VALID_DATA,
                                 CustomTestCase, authorized,
                                 with_existing_user)
from subscriptions.views.profile import ProfileView


class ProfileViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('profile')
        self.login_url = reverse('login')
        self.success_url = reverse('home')
        self.profile_initial_data = {
            'username': 'testuser30',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': '',
            'receive_emails': True,
        }
        self.profile_update_valid_data = {
            'username': 'testuser30',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }
        self.required_field_is_missing_data = {
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }
        self.username_empty_data = {
            'username': '',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }
        self.email_empty_data = {
            'username': 'testuser30',
            'email': '',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }
        self.invalid_email_data = {
            'username': 'testuser30',
            'email': 'testuser30',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }
        self.username_already_exists_data = {
            'username': 'testuser40',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }
        self.email_already_exists_data = {
            'username': 'testuser30',
            'email': 'testuser40@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'webhook_url': 'https://www.google.com.ua/',
            'receive_emails': False,
        }

    @authorized()
    def test_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ProfileView.template_name)
        self.assertIsInstance(response.context['form'], ProfileView.form_class)
        self.assertEqual(response.context['form'].cleaned_data, self.profile_initial_data)

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    @authorized(jwt_token='test_jwt_token')
    def test_get_invalid_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    @authorized(user_id=10000)
    def test_get_invalid_user_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    @authorized()
    def test_post_valid_data_authorized(self):
        response = self.client.post(self.url, self.profile_update_valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_post_valid_data_unauthorized(self):
        response = self.client.post(self.url, self.profile_update_valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    @authorized()
    def test_post_required_field_is_missing(self):
        response = self.client.post(self.url, self.required_field_is_missing_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('username', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('username'))

    @authorized()
    def test_post_username_empty(self):
        response = self.client.post(self.url, self.username_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('username', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('username'))

    @authorized()
    def test_post_email_empty(self):
        response = self.client.post(self.url, self.email_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('email', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('email'))

    @authorized()
    def test_post_invalid_email(self):
        response = self.client.post(self.url, self.invalid_email_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('email', response.context['form'].errors.keys())
        self.assertIn('Enter a valid email address.', response.context['form'].errors.get('email'))

    @authorized()
    @with_existing_user(USER_2_VALID_DATA, LOGIN_VALID_DATA2)
    def test_post_username_already_exists(self):
        response = self.client.post(self.url, self.username_already_exists_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('username', response.context['form'].errors.keys())
        self.assertIn('A user with that username already exists.', response.context['form'].errors.get('username'))

    @authorized()
    @with_existing_user(USER_2_VALID_DATA, LOGIN_VALID_DATA2)
    def test_post_email_already_exists(self):
        response = self.client.post(self.url, self.email_already_exists_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('email', response.context['form'].errors.keys())
        self.assertIn('user with this email address already exists.', response.context['form'].errors.get('email'))
