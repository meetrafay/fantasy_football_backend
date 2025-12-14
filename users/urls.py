from django.urls import path

from .views.login import LoginView
from .views.signup import SignupView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]