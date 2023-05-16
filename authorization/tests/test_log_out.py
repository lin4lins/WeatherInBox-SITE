from django.test import Client
from django.urls import reverse

from authorization.tests import CustomTestCase, authorized


class LogOutViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')
        self.success_url = reverse('login')

    @authorized()
    def test_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)
        self.assertNotIn('', response.cookies['jwt_token'])
        self.assertNotIn('', response.cookies['user_id'])

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, self.success_url)
        self.assertNotIn('', response.cookies['jwt_token'])
        self.assertNotIn('', response.cookies['user_id'])
