# Generated by Django 3.1.7 on 2021-03-31 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0004_auto_20210315_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='reply_status',
            field=models.BooleanField(default=False),
        ),
    ]
