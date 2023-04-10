from django.shortcuts import render
from django.views import View

import requests

from subscriptions.mixins import LoginRequiredMixin
from weather_reminder.settings import API_URL


class HomeView(LoginRequiredMixin, View):
    template_name = 'subscriptions/home.html'

    def get(self, request):
        user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
        current_user_response = requests.get(f'{API_URL}/users/{user_id}', headers={'Authorization': f'Bearer {jwt_token}'})
        return render(request, self.template_name, current_user_response.json())
