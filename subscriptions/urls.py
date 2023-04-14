from django.urls import path

from subscriptions.views.home import HomeView
from subscriptions.views.profile import ProfileView
from subscriptions.views.subscriptions import SubscriptionListView, SubscriptionCreateView, SubscriptionUpdateView, SubscriptionDeleteView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscription/list/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscription/update/<int:id>/', SubscriptionUpdateView.as_view(), name='subscription-update'),
    path('subscription/delete/<int:id>/', SubscriptionDeleteView.as_view(), name='subscription-delete'),
]
