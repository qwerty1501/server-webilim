# Generated by Django 3.2.7 on 2022-02-07 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0012_alter_lesson_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.PositiveSmallIntegerField(choices=[(10, 'Месяц'), (11, 'Половина курса'), (12, 'Полный курс')], default=10, verbose_name='Тип подписки')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Цена')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to='courses.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Подписка на курс',
                'verbose_name_plural': 'Подписки на курсы',
            },
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False, verbose_name='Активный?')),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_membership', to='membership.membership', verbose_name='Тип подписки')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_membership', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка пользователя',
                'verbose_name_plural': 'Подписки пользователей',
            },
        ),
    ]
