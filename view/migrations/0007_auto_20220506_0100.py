# Generated by Django 3.2.10 on 2022-05-05 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0006_event_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=models.FloatField(),
        ),
    ]