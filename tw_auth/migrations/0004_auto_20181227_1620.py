# Generated by Django 2.0.1 on 2018-12-27 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tw_auth', '0003_auto_20181226_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 27, 16, 20, 37, 322872)),
        ),
    ]
