# Generated by Django 3.1.7 on 2021-04-05 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210403_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierproduct',
            name='currency',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]