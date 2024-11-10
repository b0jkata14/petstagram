from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, DeleteView

from petstagram.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from petstagram.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register-page.html'


class AppUserLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'


class AppUserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class ProfileDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-details-page.html'


class AppUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_photos_count'] = self.object.photo_set.all().count()
        context['total_pets_count'] = self.object.pet_set.all().count()
        context['total_likes_count'] = sum(p.like_set.count() for p in self.object.photo_set.all())

        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def test_func(self):
        """Ensure that the user can only edit their own profile"""
        profile = self.get_object()
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={'pk': self.object.pk}
        )


class AppUserDeleteView(UserPassesTestMixin, DeleteView):
    model = UserModel
    success_url = reverse_lazy('home-page')
    template_name = 'accounts/profile-delete-page.html'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

# def delete_profile(request, pk):
#     return render(request, 'accounts/profile-delete-page.html')
