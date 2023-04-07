from django.urls import path

from authorization.views.log import LogInView, LogOutView
from authorization.views.signup import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('login/', LogInView.as_view(), name='log-in'),
    path('logout/', LogOutView.as_view(), name='log-out'),
]
