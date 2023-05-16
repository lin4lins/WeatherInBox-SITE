import json

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from subscriptions.forms import SubscriptionCreateForm
from subscriptions.mixins import LoginRequiredMixin
from weather_reminder.settings import API_URL


class SubscriptionListView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions.html'
    logout_url = reverse_lazy('logout')

    def get(self, request):
        user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
        subscription_list_response = requests.get(f'{API_URL}/subscriptions/',
                                                  headers={'Authorization': f'Bearer {jwt_token}'})
        if subscription_list_response.status_code != 200:
            return HttpResponseRedirect(self.logout_url)

        return render(request, self.template_name, {'subs': subscription_list_response.json()})


class SubscriptionCreateView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions-create.html'
    form_class = SubscriptionCreateForm
    success_url = reverse_lazy('subscription-list')
    logout_url = reverse_lazy('logout')

    def get(self, request):
        form = self.form_class()
        jwt_token = request.COOKIES.get('jwt_token')
        cities_response = requests.get(f'{API_URL}/cities/', headers={'Authorization': f'Bearer {jwt_token}',
                                                                    'Content-Type': 'application/json'})
        if cities_response.status_code != 200:
            return HttpResponseRedirect(self.logout_url)
        return render(request, self.template_name, {'form': form, 'cities': cities_response.json()})

    def post(self, request):
        form = self.form_class(request.POST)
        jwt_token = request.COOKIES.get('jwt_token')
        if form.is_valid():
            create_subscription_response = requests.post(f'{API_URL}/subscriptions/', data=form.get_json(),
                                                         headers={'Authorization': f'Bearer {jwt_token}',
                                                                  'Content-Type': 'application/json'})
            if create_subscription_response.status_code == 201:
                return HttpResponseRedirect(self.success_url)

            form.add_api_response_errors(create_subscription_response.json())

        cities_response = requests.get(f'{API_URL}/cities/', headers={'Authorization': f'Bearer {jwt_token}',
                                                                      'Content-Type': 'application/json'})
        return render(request, self.template_name, {'form': form, 'cities': cities_response.json()})


class SubscriptionUpdateView(LoginRequiredMixin, View):
    def post(self, request, id: int):
        is_active = request.GET.get('is_active', None)
        times_per_day = request.GET.get('times_per_day', None)
        data = {'is_active': is_active} if is_active else {'times_per_day': times_per_day} if times_per_day else {}
        jwt_token = request.COOKIES.get('jwt_token')
        partial_update_subscription_response = requests.patch(f'{API_URL}/subscriptions/{id}/',
                                                              data=json.dumps(data),
                                                              headers={'Authorization': f'Bearer {jwt_token}',
                                                                       'Content-Type': 'application/json'})
        return HttpResponse(status=partial_update_subscription_response.status_code,
                            content=partial_update_subscription_response.content)


class SubscriptionDeleteView(LoginRequiredMixin, View):
    def get(self, request, id: int):
        jwt_token = request.COOKIES.get('jwt_token')
        subscription_delete_response = requests.delete(f'{API_URL}/subscriptions/{id}/',
                                                       headers={'Authorization': f'Bearer {jwt_token}'})
        if subscription_delete_response.status_code == 204:
            return HttpResponse(status=200)

        return HttpResponse(subscription_delete_response.content, status=400)
