import json

from django.contrib.auth.forms import UserCreationForm
from django import forms

from authorization.models import User


class CustomModelForm(forms.ModelForm):
    def add_api_response_errors(self, field_errors: dict):
        for error_field, error in field_errors.items():
            if error_field not in self.fields:
                error_field = None

            self.add_error(error_field, error)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def add_response_errors(self, field_errors: dict):
        for field, error in field_errors.items():
            if field == 'password':
                self.add_error('password1', error)
                pass

            self.add_error(field, error)

    def get_json(self):
        data = {
            'username': self.cleaned_data.get('username'),
            'first_name': self.cleaned_data.get('first_name'),
            'last_name': self.cleaned_data.get('first_name'),
            'email': self.cleaned_data.get('email'),
            'password': self.cleaned_data.get('password1'),
        }
        return json.dumps(data)


class LogInForm(CustomModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
