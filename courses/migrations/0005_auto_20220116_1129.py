# Generated by Django 3.2.7 on 2022-01-16 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_course_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration_months_ky',
            field=models.CharField(max_length=200, null=True, verbose_name='Длительность в месяцах'),
        ),
        migrations.AddField(
            model_name='course',
            name='duration_months_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Длительность в месяцах'),
        ),
    ]
