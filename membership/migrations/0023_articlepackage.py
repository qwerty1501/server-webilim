# Generated by Django 3.2.7 on 2022-02-11 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20220209_0544'),
        ('membership', '0022_alter_coupon_valid_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article', verbose_name='Статья')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.package', verbose_name='Пакет')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
