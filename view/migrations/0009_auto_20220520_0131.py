# Generated by Django 3.2.10 on 2022-05-19 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('view', '0008_auto_20220513_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='turism',
            name='cat_image',
            field=models.URLField(null=True),
        ),
        migrations.CreateModel(
            name='FavouriteCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favourite', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='view.turism')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='turism',
            name='favourite_category',
            field=models.ManyToManyField(through='view.FavouriteCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]
