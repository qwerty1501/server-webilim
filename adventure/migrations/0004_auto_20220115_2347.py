# Generated by Django 3.2.7 on 2022-01-15 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0003_travelreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='subtitle_ky',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Подзаголовок'),
        ),
        migrations.AddField(
            model_name='travel',
            name='subtitle_ru',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Подзаголовок'),
        ),
    ]
