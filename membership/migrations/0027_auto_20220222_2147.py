# Generated by Django 3.2.7 on 2022-02-22 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0026_alter_registerrequest_paid_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterRequestProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Привязать существующего пользователя',
                'verbose_name_plural': 'Привязать существующих пользователей',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('membership.registerrequest',),
        ),
        migrations.AlterModelOptions(
            name='usermembership',
            options={'verbose_name': 'Пакет', 'verbose_name_plural': 'Пакеты'},
        ),
        migrations.CreateModel(
            name='RegisterRequestPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_date', models.DateField(blank=True, null=True, verbose_name='Дата покупки')),
                ('expire_date', models.DateField(blank=True, null=True, verbose_name='Срок истечения')),
                ('type', models.CharField(max_length=255, verbose_name='Тип пакета/Описание')),
                ('paid_price', models.CharField(blank=True, max_length=255, null=True, verbose_name='Конечная сумма')),
                ('reqister_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.registerrequest', verbose_name='Заявка на регистрацию')),
            ],
        ),
    ]