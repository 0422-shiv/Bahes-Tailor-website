# Generated by Django 3.1.7 on 2021-03-12 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210308_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_category_img'),
        ),
        migrations.AddField(
            model_name='product_subcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_category_img'),
        ),
    ]
