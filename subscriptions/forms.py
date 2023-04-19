import json
from authorization.forms import CustomModelForm
from authorization.models import User
from .models import Subscription


class SubscriptionCreateForm(CustomModelForm):
    class Meta:
        model = Subscription
        fields = ['city_name', 'country_name', 'times_per_day']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['city'] = {'name': cleaned_data['city_name'], 'country_name': cleaned_data['country_name']}
        cleaned_data.pop('city_name')
        cleaned_data.pop('country_name')
        return cleaned_data

    def get_json(self):
        data = {
            'city': {'name': self.cleaned_data.get('city_name', None),
                     'country_name': self.cleaned_data.get('country_name', None)},
            'times_per_day': self.cleaned_data.get('times_per_day', None)
        }
        return json.dumps(data)


class SubscriptionUpdateForm(CustomModelForm):
    class Meta:
        model = Subscription
        fields = ['times_per_day', 'is_active']


class UserUpdateForm(CustomModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',  'email', 'webhook_url', 'receive_emails']
        labels = {
            'webhook_url': 'URL'
        }
