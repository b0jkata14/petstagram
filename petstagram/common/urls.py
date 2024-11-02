from django.urls import path

from petstagram.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('like/<int:photo_id>/', views.LikeFunctionality.as_view(), name='like'),
    path('share/<int:photo_id>/', views.CopyLinkToClipboardView.as_view(), name='share'),
    path('comment/<int:photo_id>/', views.AddCommentView.as_view(), name='comment')
]
