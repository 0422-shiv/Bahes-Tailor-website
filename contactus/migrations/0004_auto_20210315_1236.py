# Generated by Django 3.1.7 on 2021-03-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0003_auto_20210315_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]