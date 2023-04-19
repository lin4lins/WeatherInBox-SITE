import json

from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from authorization.models import User


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


class LogInForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def add_response_errors(self, field_errors: dict):
        for field, error in field_errors.items():
            self.add_error(None, error)
