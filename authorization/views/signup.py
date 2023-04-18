import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from authorization.forms import SignUpForm
import requests

from weather_reminder.settings import API_URL


# Create your views here.


class SignUpView(View):
    template_name = 'authorization/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data_json = json.dumps(form.cleaned_data)
            create_user_response = requests.post(f'{API_URL}/users/', data=form_data_json,
                                                 headers={'Content-Type': 'application/json'})
            if create_user_response.status_code == 201:
                return HttpResponseRedirect(self.success_url)

            return HttpResponse(create_user_response.content)

        return HttpResponse(form.errors)
