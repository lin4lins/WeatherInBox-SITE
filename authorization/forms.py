from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
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

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['password'] = cleaned_data.get('password1', None)
        cleaned_data.pop('password1', None)
        cleaned_data.pop('password2', None)
        return cleaned_data


class LogInForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def add_response_errors(self, field_errors: dict):
        for field, error in field_errors.items():
            self.add_error(None, error)
