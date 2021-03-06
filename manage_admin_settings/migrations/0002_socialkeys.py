# Generated by Django 3.2.2 on 2021-07-10 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manage_admin_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_type', models.CharField(default='', max_length=150)),
                ('key', models.CharField(default='', max_length=500)),
                ('secret_key', models.CharField(default='', max_length=500)),
                ('updated_dt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
