# Generated by Django 2.1.7 on 2019-08-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0012_remove_teams_chemp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='birthday',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата рождения'),
        ),
    ]
