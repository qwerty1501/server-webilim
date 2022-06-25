# Generated by Django 3.2.7 on 2022-03-10 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0006_travel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='travels/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='travel',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='travels/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='travel',
            name='video',
            field=models.URLField(blank=True, null=True, verbose_name='Видео'),
        ),
    ]
