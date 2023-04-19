import json
from authorization.forms import CustomModelForm
from authorization.models import User
from .models import Subscription


class SubscriptionCreateForm(CustomModelForm):
    class Meta:
        model = Subscription
        fields = ['country_name', 'city_name', 'times_per_day']
        labels = {
            'country_name': 'Country',
            'city_name': 'City',
            'times_per_day': 'Frequency'
        }

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
