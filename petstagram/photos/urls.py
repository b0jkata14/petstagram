from django.urls import path, include

from petstagram.photos import views

urlpatterns = [
    path('add/', views.AddPhotoView.as_view(), name='photo-add'),
    path('<int:pk>/', include([
        path('', views.ShowPhotoDetailsView.as_view(), name='photo-details'),
        path('edit/', views.EditPhotoView.as_view(), name='photo-edit'),
        path('delete/', views.DeletePhotoView.as_view(), name='photo-delete')
    ]))
]