# Generated by Django 3.2.7 on 2022-01-15 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20220115_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='image',
            field=models.ImageField(null=True, upload_to='mentors/', verbose_name='Изображение'),
        ),
    ]
