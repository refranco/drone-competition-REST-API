# Generated by Django 3.2.9 on 2022-01-18 17:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('toysModel', '0010_alter_toymodel_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toymodel',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 17, 48, 40, 116967, tzinfo=utc)),
        ),
    ]
