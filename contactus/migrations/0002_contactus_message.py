# Generated by Django 3.1.7 on 2021-03-15 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='message',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
