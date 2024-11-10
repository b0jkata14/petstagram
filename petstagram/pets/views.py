from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.pets.models import Pet
from petstagram.pets.forms import PetForm, PetDeleteForm


class AddPetView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )

# def add_pet(request):
#     form = PetForm(request.POST or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('profile-details', pk=1)
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'pets/pet-add-page.html', context)


class PetDetailsView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    context_object_name = 'pet'
    slug_url_kwarg = 'pet_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_photos'] = self.object.photo_set.all()
        context['comment_form'] = CommentForm

        return context


# def show_pet_details(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     all_photos = pet.photo_set.all()
#
#     context = {
#         'pet': pet,
#         'all_photos': all_photos,
#         'comment_form': CommentForm,
#     }
#
#     return render(request, 'pets/pet-details-page.html', context=context)

class EditPetView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = 'pet_slug'

    template_name = 'pets/pet-edit-page.html'

    def test_func(self):
        owner = self.get_object().user
        return self.request.user == owner

    def get_success_url(self):
        return reverse_lazy(
            'pet-details',
            kwargs={
                'username': self.kwargs['username'],
                'pet_slug': self.kwargs['pet_slug'],
            }
        )


# def edit_pet(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('pet-details', username, pet_slug)
#
#     context = {
#         "pet": pet,
#         "form": form,
#     }
#
#     return render(request, 'pets/pet-edit-page.html', context)


class DeletePetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pet
    form_class = PetDeleteForm
    slug_url_kwarg = 'pet_slug'
    context_object_name = 'pet'

    template_name = 'pets/pet-delete-page.html'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def test_func(self):
        owner = self.get_object().user
        return self.request.user == owner

    def get_initial(self):
        return self.object.__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.get_initial(),
        })

        return kwargs


# def delete_pet(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetDeleteForm(request.POST or None, instance=pet)
#
#     if request.method == "POST":
#         pet.delete()
#         return redirect('profile-details', pk=1)
#
#     context = {
#         "form": form,
#     }
#     return render(request, 'pets/pet-delete-page.html', context)
