# Generated by Django 5.0.6 on 2024-05-17 07:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_data_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
