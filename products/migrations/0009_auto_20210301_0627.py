# Generated by Django 3.1.7 on 2021-03-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_supplierproduct_roller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierproduct',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]