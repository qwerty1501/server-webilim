# Generated by Django 3.2.7 on 2022-01-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_mentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='bio_ky',
            field=models.TextField(null=True, verbose_name='Биография'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='bio_ru',
            field=models.TextField(null=True, verbose_name='Биография'),
        ),
    ]
