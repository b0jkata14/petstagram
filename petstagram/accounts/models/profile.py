from django.contrib.auth import get_user_model
from django.db import models

from petstagram.accounts.mixins import optional_field


UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        **optional_field(),
    )

    last_name = models.CharField(
        max_length=30,
        **optional_field(),
    )

    date_of_birth = models.DateField(
        **optional_field(),
    )

    profile_picture = models.URLField(
        **optional_field(),
    )
