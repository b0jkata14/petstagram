from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoCreateForm, PhotoEditForm, PhotoDeleteForm
from petstagram.photos.models import Photo


class AddPhotoView(CreateView):
    model = Photo
    form_class = PhotoCreateForm

    template_name = 'photos/photo-add-page.html'
    success_url = reverse_lazy('home-page')


# def add_photo(request):
#     form = PhotoCreateForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
#         return redirect('home-page')
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'photos/photo-add-page.html', context)


class ShowPhotoDetailsView(DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'likes': self.object.like_set.all(),
            'comments': self.object.comment_set.all(),
            'comment_form': CommentForm(),
        })

        return context


# def show_photo_details(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     likes = photo.like_set.all()
#     comments = photo.comment_set.all()
#
#     comment_form = CommentForm()
#
#     context = {
#         'photo': photo,
#         'likes': likes,
#         'comments': comments,
#         'comment_form': comment_form,
#     }
#
#     return render(request, 'photos/photo-details-page.html', context=context)


class EditPhotoView(UpdateView):
    model = Photo
    form_class = PhotoEditForm

    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self):
        return reverse_lazy(
            'photo-details',
            kwargs={
                'pk': self.kwargs['pk'],
            }
        )


# def edit_photo(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     form = PhotoEditForm(request.POST or None, instance=photo)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('photo-details', pk)
#
#     context = {
#         "photo": photo,
#         "form": form,
#     }
#
#     return render(request, 'photos/photo-edit-page.html', context)


class DeletePhotoView(DeleteView):
    model = Photo
    form_class = PhotoDeleteForm

    success_url = reverse_lazy('home-page')
    template_name = 'photos/photo-delete-page-extra.html'

    def get_initial(self):
        return self.object.__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.get_initial(),
        })

        return kwargs


# def delete_photo(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     form = PhotoDeleteForm(request.POST or None, instance=photo)
#
#     if request.method == "POST":
#         photo.delete()
#         return redirect('home-page')
#
#     context = {
#         "photo": photo,
#         "form": form,
#     }
#
#     return render(request, 'photos/photo-delete-page-extra.html', context)