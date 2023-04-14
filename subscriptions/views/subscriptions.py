import json

import pycountry
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from subscriptions.forms import SubscriptionCreateForm, SubscriptionUpdateForm
from subscriptions.mixins import LoginRequiredMixin
from weather_reminder.settings import API_URL


class SubscriptionListView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions.html'

    def get(self, request):
        user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
        subscription_list_response = requests.get(f'{API_URL}/subscriptions/',
                                                  headers={'Authorization': f'Bearer {jwt_token}'})
        return render(request, self.template_name, {'subs': subscription_list_response.json()})


class SubscriptionCreateView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions-create.html'
    form_class = SubscriptionCreateForm

    def get(self, request):
        form = SubscriptionCreateForm()
        country_names = [country.name for country in pycountry.countries]
        return render(request, self.template_name, {'form': form, 'country_names': country_names})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            jwt_token = request.COOKIES.get('jwt_token')
            form_data_json = json.dumps(form.cleaned_data)
            create_subscription_response = requests.post(f'{API_URL}/subscriptions/', data=form_data_json,
                                                         headers={'Authorization': f'Bearer {jwt_token}',
                                                                  'Content-Type': 'application/json'})
            if create_subscription_response.status_code == 201:
                return HttpResponse('Success')

            return HttpResponse(create_subscription_response.content)

        return HttpResponse(form.errors)


class SubscriptionUpdateView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions-create.html'
    form_class = SubscriptionUpdateForm

    def post(self, request, id: int):
        request_body_str = request.body.decode('utf-8')
        request_body_dict = json.loads(request_body_str)
        form = self.form_class(request_body_dict)
        if form.is_valid():
            jwt_token = request.COOKIES.get('jwt_token')
            form_data_json = json.dumps(form.cleaned_data)
            partial_update_subscription_response = requests.patch(f'{API_URL}/subscriptions/{id}/',
                                                                  data=form_data_json,
                                                                  headers={'Authorization': f'Bearer {jwt_token}',
                                                                           'Content-Type': 'application/json'})
            if partial_update_subscription_response.status_code == 200:
                return HttpResponse(status=200)

            return HttpResponse(partial_update_subscription_response.content, status=400)

        return HttpResponse(form.errors, status=400)


class SubscriptionDeleteView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions.html'

    def get(self, request, id: int):
        jwt_token = request.COOKIES.get('jwt_token')
        subscription_delete_response = requests.delete(f'{API_URL}/subscriptions/{id}',
                                                       headers={'Authorization': f'Bearer {jwt_token}'})
        if subscription_delete_response.status_code == 204:
            return HttpResponse(status=200)

        return HttpResponse(subscription_delete_response.content, status=400)
