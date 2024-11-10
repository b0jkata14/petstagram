from django.urls import path, include

from petstagram.accounts import views
from petstagram.accounts.views import AppUserRegisterView, AppUserLoginView, AppUserLogoutView, ProfileDetailsView, \
    ProfileEditView, AppUserDetailView, AppUserDeleteView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', AppUserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', AppUserDetailView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', AppUserDeleteView.as_view(), name='profile-delete'),
    ])),
]
