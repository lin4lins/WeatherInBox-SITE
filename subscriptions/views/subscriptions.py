import json

import pycountry
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
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
    success_url = reverse_lazy('subscription-list')

    def get(self, request):
        form = SubscriptionCreateForm()
        country_names = [country.name for country in pycountry.countries]
        return render(request, self.template_name, {'form': form, 'country_names': country_names})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            jwt_token = request.COOKIES.get('jwt_token')
            create_subscription_response = requests.post(f'{API_URL}/subscriptions/', data=form.get_json(),
                                                         headers={'Authorization': f'Bearer {jwt_token}',
                                                                  'Content-Type': 'application/json'})
            if create_subscription_response.status_code == 201:
                return HttpResponseRedirect(self.success_url)

            form.add_api_response_errors(create_subscription_response.json())

        return render(request, self.template_name, {'form': form})


class SubscriptionUpdateView(LoginRequiredMixin, View):
    template_name = 'subscriptions/subscriptions-create.html'

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
    template_name = 'subscriptions/subscriptions.html'

    def get(self, request, id: int):
        jwt_token = request.COOKIES.get('jwt_token')
        subscription_delete_response = requests.delete(f'{API_URL}/subscriptions/{id}',
                                                       headers={'Authorization': f'Bearer {jwt_token}'})
        if subscription_delete_response.status_code == 204:
            return HttpResponse(status=200)

        return HttpResponse(subscription_delete_response.content, status=400)
