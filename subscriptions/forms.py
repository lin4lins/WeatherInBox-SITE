import json

from django import forms

from authorization.forms import CustomModelForm
from authorization.models import User

from .models import Subscription


class SubscriptionCreateForm(CustomModelForm):
    city_id = forms.IntegerField(error_messages={'invalid': 'Please select a location.'})

    class Meta:
        model = Subscription
        fields = ['city_id', 'times_per_day']

    def get_json(self):
        return json.dumps(self.cleaned_data)


class UpdateProfileForm(CustomModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'webhook_url', 'receive_emails']
        labels = {
            'webhook_url': 'URL'
        }
