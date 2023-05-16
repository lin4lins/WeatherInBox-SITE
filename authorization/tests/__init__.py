import json

import requests
from django.test import TestCase

from weather_reminder.settings import API_URL

USER_VALID_DATA = {
    'username': 'testuser30',
    'email': 'testuser30@example.com',
    'first_name': 'Test',
    'last_name': 'Tester',
    'password': 'testPassword99',
}

USER_2_VALID_DATA = {
    'username': 'testuser40',
    'email': 'testuser40@example.com',
    'first_name': 'Test',
    'last_name': 'Tester',
    'password': 'testPassword99',
}

LOGIN_VALID_DATA = {
    'username': 'testuser30',
    'password': 'testPassword99'
}

LOGIN_VALID_DATA2 = {
    'username': 'testuser40',
    'password': 'testPassword99'
}


class CustomTestCase(TestCase):
    user_id = None
    jwt_token = None

    @classmethod
    def setUpClass(cls):
        create_user(USER_VALID_DATA)
        cls.user_id, cls.jwt_token = login_user(LOGIN_VALID_DATA)

    @classmethod
    def tearDownClass(cls):
        delete_user(cls.user_id, cls.jwt_token)


def create_user(user_create_data):
    create_response = requests.post(f'{API_URL}/users/', data=json.dumps(user_create_data),
                                    headers={'Content-Type': 'application/json'})
    if create_response.status_code != 201:
        raise Exception(f'create_response.status_code {create_response.status_code} != 201')


def login_user(login_data):
    login_response = requests.post(f'{API_URL}/token/', data=json.dumps(login_data),
                                   headers={'Content-Type': 'application/json'})
    if login_response.status_code != 200:
        raise Exception(f'create_response.status_code {login_response.status_code} != 200')

    user_id = login_response.json().get('user_id')
    jwt_token = login_response.json().get('access')
    return user_id, jwt_token


def delete_user(user_id, jwt_token):
    delete_response = requests.delete(f'{API_URL}/users/{user_id}/',
                                      headers={'Authorization': f'Bearer {jwt_token}'})
    if delete_response.status_code != 204:
        raise Exception(f'delete_response.status_code {delete_response.status_code} != 204')


def authorized(user_id=None, jwt_token=None):
    def wrapper(func):
        def inner_wrapper(obj, *args, **kwargs):
            obj.client.cookies.load({
                'user_id': user_id or obj.user_id,
                'jwt_token': jwt_token or obj.jwt_token
            })
            func(obj, *args, **kwargs)
            obj.client.cookies.clear()
        return inner_wrapper
    return wrapper


def with_existing_user(user_create_data, user_login_data):
    def wrapper(func):
        def inner_wrapper(obj, *args, **kwargs):
            create_user(user_create_data)
            func(obj, *args, **kwargs)
            user_id, jwt_token = login_user(user_login_data)
            delete_user(user_id, jwt_token)
        return inner_wrapper
    return wrapper
