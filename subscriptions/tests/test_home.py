from django.test import Client
from django.urls import reverse

from authorization.tests import CustomTestCase, authorized
from subscriptions.views.home import HomeView


class HomeViewViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.login_url = reverse('login')

    @authorized()
    def test_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HomeView.template_name)

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
