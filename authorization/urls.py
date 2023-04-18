from django.urls import path

from authorization.views.log import LogInView, LogOutView
from authorization.views.signup import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]
