# Generated by Django 3.1.7 on 2021-02-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_supplierproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplierproduct',
            name='season',
        ),
        migrations.AddField(
            model_name='supplierproduct',
            name='season',
            field=models.ManyToManyField(blank=True, null=True, to='products.Season'),
        ),
    ]
