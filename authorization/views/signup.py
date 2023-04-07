
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from authorization.forms import SignUpForm
import requests

from weather_reminder.settings import API_URL


# Create your views here.


class SignUpView(View):
    template_name = 'authorization/signup.html'
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            create_user_response = requests.post(f'{API_URL}/users/', data=form.cleaned_data)
            if create_user_response.status_code == 201:
                return HttpResponse('Success')

            return HttpResponse(create_user_response.content)

        return HttpResponse(form.errors)
