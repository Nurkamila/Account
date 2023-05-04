from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('confirm-email/', ActivationView.as_view()),
    path('reset_password_email/', ResetPasswordEmailView.as_view()),
    path('reset_password/<code>/', ResetPasswordView.as_view()),
]