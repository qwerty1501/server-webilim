# Generated by Django 3.2.7 on 2022-02-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_customuser_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название компании/Род деятельности'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='expertise',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Экспертиза'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='expertise_description',
            field=models.TextField(blank=True, null=True, verbose_name='Чем вы занимаетесь?'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=32, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Инстаграм'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='Линкедин'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Род деятельности'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram',
            field=models.URLField(blank=True, null=True, verbose_name='Телеграм'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='timezone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Часовой пояс'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='web_site',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Веб-сайт'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='whatsapp',
            field=models.URLField(blank=True, null=True, verbose_name='Вотсап'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='youtube',
            field=models.URLField(blank=True, null=True, verbose_name='Ютуб'),
        ),
    ]
