# Generated by Django 3.2.7 on 2022-01-19 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20220119_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='title_ky',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Заголовок'),
        ),
    ]
