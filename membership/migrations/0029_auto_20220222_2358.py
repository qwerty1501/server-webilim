# Generated by Django 3.2.7 on 2022-02-22 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0028_auto_20220222_2247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registerrequestpayment',
            options={'verbose_name': 'Оплата пользователя', 'verbose_name_plural': 'Оплаты пользователей'},
        ),
        migrations.AlterModelOptions(
            name='usermembership',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterField(
            model_name='registerrequestpayment',
            name='register_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rg_payments', to='membership.registerrequest', verbose_name='Заявка на регистрацию'),
        ),
    ]
