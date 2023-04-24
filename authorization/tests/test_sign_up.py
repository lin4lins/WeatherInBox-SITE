from django.test import Client, TestCase
from django.urls import reverse

from authorization.forms import SignUpForm
from authorization.tests import (LOGIN_VALID_DATA, USER_VALID_DATA,
                                 delete_user, login_user, with_existing_user)
from authorization.views.sign_up import SignUpView


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')
        self.success_url = reverse('login')
        self.valid_data = {
            'username': 'testuser30',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }
        self.required_field_is_missing_data = {
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }
        self.username_empty_data = {
            'username': '',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }
        self.email_empty_data = {
            'username': 'testuser30',
            'email': '',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }
        self.invalid_email_data = {
            'username': 'testuser30',
            'email': 'testuser30',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }
        self.passwords_missmatch_data = {
            'username': 'testuser30',
            'email': 'testuser26@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword98',
        }
        self.weak_passwords_data = {
            'username': 'testuser30',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': '1',
            'password2': '1',
        }
        self.username_already_exists_data = {
            'username': 'testuser30',
            'email': 'testuser31@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }
        self.email_already_exists_data = {
            'username': 'testuser31',
            'email': 'testuser30@example.com',
            'first_name': 'Test',
            'last_name': 'Tester',
            'password1': 'testPassword99',
            'password2': 'testPassword99',
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, SignUpView.template_name)
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_post_valid_data(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)
        user_id, jwt_token = login_user(LOGIN_VALID_DATA)
        delete_user(user_id, jwt_token)

    def test_post_required_field_is_missing(self):
        response = self.client.post(self.url, self.required_field_is_missing_data)
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

    def test_post_email_empty(self):
        response = self.client.post(self.url, self.email_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('email', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('email'))

    def test_post_invalid_email(self):
        response = self.client.post(self.url, self.invalid_email_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('email', response.context['form'].errors.keys())
        self.assertIn('Enter a valid email address.', response.context['form'].errors.get('email'))

    def test_post_passwords_missmatch(self):
        response = self.client.post(self.url, self.passwords_missmatch_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('password2', response.context['form'].errors.keys())
        self.assertIn('The two password fields didn’t match.', response.context['form'].errors.get('password2'))

    def test_post_weak_passwords(self):
        response = self.client.post(self.url, self.weak_passwords_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('password2', response.context['form'].errors.keys())
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      response.context['form'].errors.get('password2'))
        self.assertIn('This password is too common.', response.context['form'].errors.get('password2'))
        self.assertIn('This password is entirely numeric.', response.context['form'].errors.get('password2'))

    @with_existing_user(USER_VALID_DATA, LOGIN_VALID_DATA)
    def test_post_username_already_exists(self):
        response = self.client.post(self.url, self.username_already_exists_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('username', response.context['form'].errors.keys())
        self.assertIn('A user with that username already exists.', response.context['form'].errors.get('username'))

    @with_existing_user(USER_VALID_DATA, LOGIN_VALID_DATA)
    def test_post_email_already_exists(self):
        response = self.client.post(self.url, self.email_already_exists_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('email', response.context['form'].errors.keys())
        self.assertIn('user with this email address already exists.', response.context['form'].errors.get('email'))
