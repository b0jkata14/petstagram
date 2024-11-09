from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from petstagram.accounts.forms import AppUserCreationForm, AppUserLoginForm

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register-page.html'


class AppUserLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'


class AppUserLogoutView(LogoutView):
    pass


def show_profile_details(request, pk):
    return render(request, 'accounts/profile-details-page.html')


def edit_profile(request, pk):
    return render(request, 'accounts/profile-edit-page.html')


def delete_profile(request, pk):
    return render(request, 'accounts/profile-delete-page.html')
