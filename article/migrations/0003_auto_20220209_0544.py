# Generated by Django 3.2.7 on 2022-02-08 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20220209_0542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Изображение'),
        ),
    ]