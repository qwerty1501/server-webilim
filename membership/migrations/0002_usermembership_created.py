# Generated by Django 3.2.7 on 2022-02-07 16:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 2, 7, 16, 6, 57, 939002, tzinfo=utc), verbose_name='Дата подписки'),
            preserve_default=False,
        ),
    ]
