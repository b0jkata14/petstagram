# Generated by Django 5.1.1 on 2024-10-13 17:33

import petstagram.photos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='media/images/', validators=[petstagram.photos.validators.FileSizeValidator(5)]),
        ),
    ]
