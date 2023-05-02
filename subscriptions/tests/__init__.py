import json

import requests

from weather_reminder.settings import API_URL

SUBSCRIPTION_VALID_DATA = {
    'city_id': 500,
    'times_per_day': 2
}


def with_existing_subscription():
    def wrapper(func):
        def inner_wrapper(obj, *args, **kwargs):
            subscription_id = create_subscription(SUBSCRIPTION_VALID_DATA, obj.jwt_token)
            func(obj, subscription_id, *args, **kwargs)
            delete_subscription(subscription_id, obj.jwt_token)
        return inner_wrapper
    return wrapper


def create_subscription(subscription_create_data, jwt_token: str):
    create_response = requests.post(f'{API_URL}/subscriptions/', data=json.dumps(subscription_create_data),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': f'Bearer {jwt_token}'})
    if create_response.status_code != 201:
        raise Exception(f'create_response.status_code {create_response.status_code} != 201')

    return create_response.json().get('id')


def delete_subscription(id: int, jwt_token: str):
    delete_response = requests.delete(f'{API_URL}/subscriptions/{id}/',
                                      headers={'Authorization': f'Bearer {jwt_token}'})
    if delete_response.status_code != 204:
        raise Exception(f'delete_response.status_code {delete_response.status_code} != 204')


