# Generated by Django 2.1.2 on 2018-12-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Location', '0012_messageticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='title',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
