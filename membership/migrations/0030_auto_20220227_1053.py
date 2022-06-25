# Generated by Django 3.2.7 on 2022-02-27 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0029_auto_20220222_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='description',
            field=models.TextField(default='def', verbose_name='Описание/Состав пакета'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(10, 'Месяц'), (13, 'Год'), (14, 'Год+')], default=10, verbose_name='Тип пакета'),
        ),
    ]