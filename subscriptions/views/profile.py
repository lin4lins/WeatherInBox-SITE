import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from subscriptions.forms import UpdateProfileForm
from subscriptions.mixins import LoginRequiredMixin
from weather_reminder.settings import API_URL


class ProfileView(LoginRequiredMixin, View):
    template_name = 'subscriptions/profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('home')
    logout_url = reverse_lazy('logout')

    def get(self, request):
        user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
        current_user_response = requests.get(f'{API_URL}/users/{user_id}/',
                                             headers={'Authorization': f'Bearer {jwt_token}'})
        if current_user_response.status_code != 200:
            return HttpResponseRedirect(self.logout_url)

        filled_form = self.form_class(current_user_response.json())
        return render(request, self.template_name, {'form': filled_form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_id, jwt_token = request.COOKIES.get('user_id'), request.COOKIES.get('jwt_token')
            partial_update_user_response = requests.patch(f'{API_URL}/users/{user_id}/', data=form.get_json(),
                                                          headers={'Authorization': f'Bearer {jwt_token}',
                                                                   'Content-Type': 'application/json'})
            if partial_update_user_response.status_code == 200:
                return HttpResponseRedirect(self.success_url)

            form.add_api_response_errors(partial_update_user_response.json())

        return render(request, self.template_name, {'form': form})
