# Generated by Django 3.2.9 on 2022-01-21 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('toysModel', '0013_alter_toymodel_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toymodel',
            name='release_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
