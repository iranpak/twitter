# Generated by Django 2.1.4 on 2018-12-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tw_auth', '0004_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='title',
            field=models.CharField(default='Tweet', max_length=32),
        ),
    ]