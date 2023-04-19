from django.urls import path

from authorization.views.log_in_out import LogInView, LogOutView
from authorization.views.sign_up import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]
