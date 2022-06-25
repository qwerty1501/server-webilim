# Generated by Django 3.2.7 on 2022-02-10 16:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0012_coursepackage_masterclasspackage_webinarpackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Купон/Промокод')),
                ('valid_from', models.DateTimeField(auto_now=True, verbose_name='Действует от')),
                ('valid_to', models.DateTimeField(verbose_name='Действует до')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField(default=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='membership.package', verbose_name='Пакет')),
            ],
        ),
    ]
