# Generated by Django 3.2.7 on 2022-04-06 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_alter_courseprogress_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseprogress',
            name='data',
        ),
    ]
