# Generated by Django 3.1.7 on 2021-04-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20210318_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MuteChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiving_mess_sound', models.URLField(blank=True, null=True)),
                ('sending_mess_sound', models.URLField(blank=True, null=True)),
                ('mute_status', models.BooleanField(default=False)),
            ],
        ),
    ]
