# Generated by Django 3.1.7 on 2021-03-03 10:05

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210301_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_category',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='category_name'),
        ),
        migrations.AddField(
            model_name='product_subcategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='subcategory_name'),
        ),
    ]