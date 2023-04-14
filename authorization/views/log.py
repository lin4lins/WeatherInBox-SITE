import datetime
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from authorization.forms import LogInForm
import requests

from weather_reminder.settings import API_URL


class LogInView(View):
    template_name = 'authorization/login.html'
    form_class = LogInForm
    success_url = '/home/'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data_json = json.dumps(form.cleaned_data)
            login_response = requests.post(f'{API_URL}/token/', data=form_data_json,
                                           headers={'Content-Type': 'application/json'})
            if login_response.status_code == 200:
                response = HttpResponseRedirect(self.success_url)
                response.set_cookie(key='jwt_token',
                                    value=login_response.json().get('access'),
                                    max_age=datetime.timedelta(days=1))
                response.set_cookie(key='user_id',
                                    value=login_response.json().get('user_id'),
                                    max_age=datetime.timedelta(days=1))
                return response

            return HttpResponse(login_response.content)

        return HttpResponse(form.errors)


class LogOutView(View):
    template_name = 'authorization/logout.html'
    success_url = '/home/'

    def get(self, request):
        response = HttpResponseRedirect(self.success_url)
        response.delete_cookie('jwt_token')
        response.delete_cookie('user_id')
        return response
