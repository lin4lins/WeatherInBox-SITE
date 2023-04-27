import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from subscriptions.mixins import LoginRequiredMixin
from weather_reminder.settings import API_URL


class HomeView(LoginRequiredMixin, View):
    template_name = 'subscriptions/home.html'
    logout_url = reverse_lazy('logout')

    def get(self, request):
        user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
        current_user_response = requests.get(f'{API_URL}/users/{user_id}/',
                                             headers={'Authorization': f'Bearer {jwt_token}'})
        if current_user_response.status_code != 200:
            return HttpResponseRedirect(self.logout_url)

        return render(request, self.template_name, {'user': current_user_response.json()})
