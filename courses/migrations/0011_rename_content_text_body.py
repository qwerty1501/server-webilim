# Generated by Django 3.2.7 on 2022-01-20 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20220119_1847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='text',
            old_name='content',
            new_name='body',
        ),
    ]
