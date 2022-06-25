# Generated by Django 3.2.7 on 2022-01-15 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_helpinchoosing_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('bio', models.TextField(verbose_name='Биография')),
            ],
            options={
                'verbose_name': 'Ментор',
                'verbose_name_plural': 'Ментора',
            },
        ),
    ]