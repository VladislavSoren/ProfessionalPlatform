
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    LoginView,
    LogoutView, RegisterView,
)
from django.contrib.auth.views import (
    # LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = "auth_block"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", TemplateView.as_view(template_name="auth_block/me.html"), name="about-me"),


    path('password-reset/', PasswordResetView.as_view(template_name='auth_block/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='auth_block/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='auth_block/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='auth_block/password_reset_complete.html'),
         name='password_reset_complete'),
]

