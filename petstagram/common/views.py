from django.utils import timezone
import pytz

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, resolve_url
from django.views import View
from django.views.generic import ListView, FormView
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


class HomePageView(ListView):
    model = Photo
    context_object_name = 'all_photos'
    template_name = 'common/home-page.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = CommentForm
        context['search_form'] = SearchForm(self.request.GET)

        # user = self.request.user
        #
        # for photo in context['all_photos']:
        #     photo.has_liked = photo.like_set.filter(user=user).exists() if user.is_authenticated else False

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(
                tagged_pets__name__icontains=pet_name
            ).distinct().order_by('-date_of_publication')

        return queryset


# def home_page(request):
#     all_photos = Photo.objects.all()
#     comment_form = CommentForm()
#     search_form = SearchForm(request.GET)
#
#     if search_form.is_valid():
#         if search_form.cleaned_data['pet_name'] != '':
#             all_photos = all_photos.filter(
#                 tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
#             )
#
#     photos_per_page = 1
#     paginator = Paginator(all_photos, photos_per_page)
#     page = request.GET.get('page')
#
#     context = {
#         'all_photos': paginator.get_page(page),
#         'comment_form': comment_form,
#         'search_form': search_form,
#     }
#
#     return render(request, 'common/home-page.html', context)

class LikeFunctionality(LoginRequiredMixin, View):
    def get(self, request, photo_id, *args, **kwargs):
        photo = Photo.objects.get(id=photo_id)
        liked_object = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()

        if liked_object:
            liked_object.delete()
        else:
            like = Like(to_photo=photo, user=request.user)
            like.save()

        return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")

# def like_functionality(request, photo_id):
#     photo = Photo.objects.get(id=photo_id)
#     liked_object = Like.objects.filter(to_photo_id=photo_id).first()
#
#     if liked_object:
#         liked_object.delete()
#     else:
#         like = Like(to_photo=photo)
#         like.save()
#
#     return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


class CopyLinkToClipboardView(View):
    def get(self, request, *args, **kwargs):
        copy(request.META['HTTP_HOST'] + resolve_url('photo-details', self.kwargs['photo_id']))

        return redirect(self.request.META['HTTP_REFERER'] + f"#{self.kwargs['photo_id']}")


# def copy_link_to_clipboard(request, photo_id):
#     copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))
#
#     return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


class AddCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = Photo.objects.get(pk=kwargs['photo_id'])
            comment.user = request.user

            # my_timezone = pytz.timezone('Europe/Sofia')
            # comment.date_time_of_publication = timezone.now().astimezone(my_timezone)

            comment.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return str((self.request.META['HTTP_REFERER'] + f"#{self.kwargs['photo_id']}"))

# def add_comment(request, photo_id):
#     if request.method == "POST":
#         photo = Photo.objects.get(pk=photo_id)
#         form = CommentForm(request.POST)
#
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.to_photo = photo
#             comment.save()
#
#         return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
