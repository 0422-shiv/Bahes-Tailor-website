# Generated by Django 3.1.4 on 2021-02-22 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210222_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='verify_status',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]