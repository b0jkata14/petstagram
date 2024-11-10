# Generated by Django 5.1.3 on 2024-11-10 12:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('photos', '0002_photo_user'), ('photos', '0003_alter_photo_options'), ('photos', '0004_alter_photo_options'), ('photos', '0005_alter_photo_options'), ('photos', '0006_alter_photo_options')]

    dependencies = [
        ('photos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={},
        ),
    ]
