# Generated by Django 3.1.7 on 2021-03-18 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatsystem_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsystem',
            name='read_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
