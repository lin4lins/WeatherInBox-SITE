from django.urls import path

from subscriptions.views.home import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]
