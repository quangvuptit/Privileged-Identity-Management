# Generated by Django 2.1.2 on 2018-11-08 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0002_accessssh_blacklist_logcommand_logininfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessssh',
            name='ssh',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ssh.SSH'),
        ),
    ]
