# Generated by Django 2.1.2 on 2018-11-11 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0005_timeblacklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeblacklist',
            name='endTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='timeblacklist',
            name='startTime',
            field=models.TimeField(),
        ),
    ]
