# Generated by Django 3.1.7 on 2021-03-18 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20210318_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsystem',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room', to='chat.room'),
        ),
    ]
