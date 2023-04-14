import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from subscriptions.forms import UserUpdateForm
from subscriptions.mixins import LoginRequiredMixin
from weather_reminder.settings import API_URL


class ProfileView(LoginRequiredMixin, View):
    template_name = 'subscriptions/profile.html'
    form_class = UserUpdateForm

    def get(self, request):
        form = UserUpdateForm()
        user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
        current_user_response = requests.get(f'{API_URL}/users/{user_id}',
                                             headers={'Authorization': f'Bearer {jwt_token}'})
        return render(request, self.template_name, {'form': form, 'user': current_user_response.json()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
            form_data_json = json.dumps(form.cleaned_data)
            partial_update_user_response = requests.patch(f'{API_URL}/users/{user_id}/', data=form_data_json,
                                                          headers={'Authorization': f'Bearer {jwt_token}',
                                                                   'Content-Type': 'application/json'})
            if partial_update_user_response.status_code == 200:
                return HttpResponse('Success')

            return HttpResponse(partial_update_user_response.content)

        return HttpResponse(form.errors)
