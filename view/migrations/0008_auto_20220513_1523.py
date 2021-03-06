# Generated by Django 3.2.10 on 2022-05-13 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0007_auto_20220506_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=50, verbose_name='city')),
            ],
        ),
        migrations.AddField(
            model_name='places',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='view.city', verbose_name='city'),
        ),
    ]
