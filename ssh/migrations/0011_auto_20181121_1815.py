# Generated by Django 2.1.2 on 2018-11-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0010_auto_20181121_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logcommand',
            name='command',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
