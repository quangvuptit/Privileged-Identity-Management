# Generated by Django 2.1.2 on 2018-10-29 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('Location', '0008_auto_20181029_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, null=True)),
                ('port', models.IntegerField(default=22, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Location.Area')),
            ],
        ),
        migrations.CreateModel(
            name='SSHPermission',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('permission', models.BooleanField(default=False)),
                ('sshconnection', models.ManyToManyField(to='ssh.SSH')),
            ],
        ),
    ]
