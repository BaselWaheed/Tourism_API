# Generated by Django 3.2.10 on 2022-05-19 23:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('view', '0009_auto_20220520_0131'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavouriteCategory',
            new_name='InterrestCategory',
        ),
    ]
