from django.forms import ModelForm

from authorization.models import User


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class LogInForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
