import json

from django.test import Client
from django.urls import reverse

from authorization.tests import CustomTestCase, authorized
from subscriptions.tests import (SUBSCRIPTION_VALID_DATA, create_subscription,
                                 delete_subscription,
                                 with_existing_subscription)
from subscriptions.views.subscriptions import (SubscriptionCreateView,
                                               SubscriptionListView)


class SubscriptionListViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('subscription-list')
        self.login_url = reverse('login')

    @authorized()
    def test_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, SubscriptionListView.template_name)
        self.assertEqual(len(response.context['subs']), 0)

    @authorized()
    @with_existing_subscription()
    def test_get_has_subscriptions_authorized(self, sub_id: int):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, SubscriptionListView.template_name)
        self.assertEqual(len(response.context['subs']), 1)
        self.assertEqual(response.context['subs'][0]['id'], sub_id)
        self.assertEqual(response.context['subs'][0]['city']['name'], SUBSCRIPTION_VALID_DATA['city']['name'])
        self.assertEqual(response.context['subs'][0]['city']['country_name'],
                         SUBSCRIPTION_VALID_DATA['city']['country_name'])

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    @authorized(jwt_token='test_jwt_token')
    def test_get_invalid_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class SubscriptionCreateViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('subscription-create')
        self.success_url = reverse('subscription-list')
        self.login_url = reverse('login')
        self.valid_data = {
            'city_name': 'Kyiv',
            'country_name': 'Ukraine',
            'times_per_day': 2
        }
        self.required_field_is_missing_data = {
            'city_name': 'Kyiv',
            'times_per_day': 2
        }
        self.city_name_empty_data = {
            'city_name': '',
            'country_name': 'Ukraine',
            'times_per_day': 2
        }
        self.country_name_empty_data = {
            'city_name': 'Kyiv',
            'country_name': '',
            'times_per_day': 2
        }
        self.not_existing_city_data = {
            'city_name': 'Test99',
            'country_name': 'Ukraine',
            'times_per_day': 2
        }
        self.not_existing_country_data = {
            'city_name': 'Kyiv',
            'country_name': 'Test99',
            'times_per_day': 2
        }
        self.times_per_day_out_of_range_number_data = {
            'city_name': 'Kyiv',
            'country_name': 'Ukraine',
            'times_per_day': 99
        }
        self.times_per_day_not_number_data = {
            'city_name': 'Kyiv',
            'country_name': 'Ukraine',
            'times_per_day': '#'
        }

    @authorized()
    def test_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, SubscriptionCreateView.template_name)
        self.assertIsInstance(response.context['form'], SubscriptionCreateView.form_class)
        self.assertIn('country_names', response.context)

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    @authorized()
    def test_post_valid_data_authorized(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

    def test_post_valid_data_unauthorized(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    @authorized()
    def test_post_required_field_is_missing(self):
        response = self.client.post(self.url, self.required_field_is_missing_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('country_name', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('country_name'))

    @authorized()
    def test_post_city_name_empty(self):
        response = self.client.post(self.url, self.city_name_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('city_name', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('city_name'))

    @authorized()
    def test_post_country_name_empty(self):
        response = self.client.post(self.url, self.country_name_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('country_name', response.context['form'].errors.keys())
        self.assertIn('This field is required.', response.context['form'].errors.get('country_name'))

    @authorized()
    def test_post_not_existing_city(self):
        response = self.client.post(self.url, self.not_existing_city_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('city_name', response.context['form'].errors.keys())
        self.assertIn('Not found.', response.context['form'].errors.get('city_name'))

    @authorized()
    def test_post_not_existing_country(self):
        response = self.client.post(self.url, self.not_existing_country_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('country_name', response.context['form'].errors.keys())
        self.assertIn('Not found.', response.context['form'].errors.get('country_name'))

    @authorized()
    def test_post_times_per_day_out_of_range_number(self):
        response = self.client.post(self.url, self.times_per_day_out_of_range_number_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('times_per_day', response.context['form'].errors.keys())
        self.assertIn('Ensure this value is less than or equal to 12.',
                      response.context['form'].errors.get('times_per_day'))

    @authorized()
    def test_post_times_per_day_not_number(self):
        response = self.client.post(self.url, self.times_per_day_not_number_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('times_per_day', response.context['form'].errors.keys())
        self.assertIn('Enter a whole number.',
                      response.context['form'].errors.get('times_per_day'))

    @authorized()
    @with_existing_subscription()
    def test_post_subscription_already_exists(self, sub_id: int):
        response = self.client.post(self.url, self.valid_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(len(response.context['form'].errors.keys()), 1)
        self.assertIn('__all__', response.context['form'].errors.keys())
        self.assertIn('The subscription with these fields already exists.',
                      response.context['form'].errors.get('__all__'))


class SubscriptionUpdateViewTestCase(CustomTestCase):
    subscription_id = None

    def setUp(self):
        self.client = Client()
        self.url_name = 'subscription-update'
        self.login_url = reverse('login')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subscription_id = create_subscription(SUBSCRIPTION_VALID_DATA, cls.jwt_token)

    @classmethod
    def tearDownClass(cls):
        delete_subscription(cls.subscription_id, cls.jwt_token)
        super().tearDownClass()

    @authorized()
    def test_post_deactivate_authorized(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?is_active=False')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get('is_active'), False)
        self.client.post(f'{url}?is_active=True')

    def test_post_deactivate_unauthorized(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?is_active=False')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={url}%3Fis_active%3DFalse')

    @authorized()
    def test_post_activate(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?is_active=True')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get('is_active'), True)

    @authorized()
    def test_post_update_times_per_day_valid(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?times_per_day=8')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get('times_per_day'), 8)
        self.client.post(f'{url}?times_per_day={SUBSCRIPTION_VALID_DATA["times_per_day"]}')

    @authorized()
    def test_post_times_per_day_out_of_range(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?times_per_day=99')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_dict.get('times_per_day')[0], 'Ensure this value is less than or equal to 12.')

    @authorized()
    def test_post_times_per_day_invalid(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?times_per_day=#')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get('times_per_day'), 2)

    @authorized()
    def test_post_subscription_not_exists(self):
        url = reverse(self.url_name, args=[10000])
        response = self.client.post(f'{url}?is_active=False')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_dict.get('detail'), 'Not found.')

    @authorized()
    def test_post_empty(self):
        url = reverse(self.url_name, args=[self.subscription_id])
        response = self.client.post(f'{url}?times_per_day=')
        response_body_str = response.content.decode('utf-8')
        response_dict = json.loads(response_body_str)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict.get('times_per_day'), 2)


class SubscriptionDeleteViewTestCase(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.url_name = 'subscription-delete'
        self.login_url = reverse('login')

    @authorized()
    def test_get_authorized(self):
        sub_id = create_subscription(SUBSCRIPTION_VALID_DATA, self.jwt_token)
        url = reverse(self.url_name, args=[sub_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @with_existing_subscription()
    def test_get_unauthorized(self, sub_id: int):
        url = reverse(self.url_name, args=[sub_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={url}')

    @with_existing_subscription()
    @authorized(jwt_token='test_jwt_token')
    def test_get_invalid_token(self, sub_id: int):
        url = reverse(self.url_name, args=[sub_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    @authorized()
    def test_get_subscription_not_exists(self):
        url = reverse(self.url_name, args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
