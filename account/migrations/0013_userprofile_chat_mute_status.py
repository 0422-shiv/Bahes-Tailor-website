# Generated by Django 3.1.7 on 2021-04-21 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20210420_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='chat_mute_status',
            field=models.BooleanField(default=True),
        ),
    ]
