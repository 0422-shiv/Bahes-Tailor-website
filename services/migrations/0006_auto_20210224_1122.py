# Generated by Django 3.1.7 on 2021-02-24 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20210224_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierservices',
            name='tailor_speci_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_tailor_speci', to='services.tailorspecification'),
        ),
    ]
