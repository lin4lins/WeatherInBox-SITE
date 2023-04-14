from django import forms

from authorization.models import User
from .models import Subscription


class SubscriptionCreateForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = ['city_name', 'country_name', 'times_per_day']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['city'] = {'name': cleaned_data['city_name'], 'country_name': cleaned_data['country_name']}
        cleaned_data.pop('city_name')
        cleaned_data.pop('country_name')
        return cleaned_data


class SubscriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['times_per_day', 'is_active']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',  'email', 'webhook_url', 'receive_emails']

