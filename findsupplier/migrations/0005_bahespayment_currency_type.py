# Generated by Django 3.1.7 on 2021-05-03 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findsupplier', '0004_auto_20210503_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='bahespayment',
            name='currency_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
