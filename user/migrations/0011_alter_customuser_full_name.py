# Generated by Django 3.2.7 on 2022-02-08 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20220209_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Полное имя'),
        ),
    ]
