# Generated by Django 3.2.9 on 2021-11-19 15:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('toysModel', '0006_alter_toymodel_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toymodel',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 15, 33, 36, 626329, tzinfo=utc)),
        ),
    ]
