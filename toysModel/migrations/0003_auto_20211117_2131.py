# Generated by Django 3.2.9 on 2021-11-17 21:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('toysModel', '0002_alter_toymodel_release_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toymodel',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='toymodel',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 17, 21, 31, 59, 231767, tzinfo=utc)),
        ),
    ]
