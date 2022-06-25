# Generated by Django 3.2.7 on 2022-02-07 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_alter_lesson_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='format',
            field=models.PositiveSmallIntegerField(choices=[(20, 'Онлайн'), (30, 'Оффлайн')], default=20, verbose_name='Формат проведения курса'),
        ),
    ]