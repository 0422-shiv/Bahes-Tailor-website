# Generated by Django 3.1.7 on 2021-03-01 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210301_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierproduct',
            name='roller',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]