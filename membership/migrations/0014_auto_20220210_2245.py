# Generated by Django 3.2.7 on 2022-02-10 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0013_coupon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'Купон', 'verbose_name_plural': 'Купоны'},
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Купон/Промокод'),
        ),
    ]