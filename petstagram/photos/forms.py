from django import forms

from petstagram.photos.models import Photo


class PhotoCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('user',)


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['photo', 'user']


class PhotoDeleteForm(PhotoCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'
