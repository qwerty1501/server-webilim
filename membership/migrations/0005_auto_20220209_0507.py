# Generated by Django 3.2.7 on 2022-02-08 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20220208_0301'),
        ('membership', '0004_package'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Membership',
            new_name='CourseMembership',
        ),
        migrations.AlterModelOptions(
            name='usermembership',
            options={'verbose_name': 'Подписка на курс', 'verbose_name_plural': 'Подписки на курсы'},
        ),
        migrations.RenameField(
            model_name='usermembership',
            old_name='membership',
            new_name='course_membership',
        ),
        migrations.AddField(
            model_name='usermembership',
            name='package_membership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_package', to='membership.package', verbose_name='Тип подписки'),
        ),
    ]
