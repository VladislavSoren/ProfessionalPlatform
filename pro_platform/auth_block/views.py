from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auth_block.forms import AuthenticationForm, UserCreationForm

from .tasks import welcome_user


class LoginView(LoginViewGeneric):
    template_name = "auth_block/login.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("auth_block:about-me")


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("auth_block:about-me")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth_block/register.html"
    success_url = reverse_lazy("auth_block:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        welcome_user.delay(self.object.pk)
        # user: AbstractUser = self.object
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user: AbstractUser = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response