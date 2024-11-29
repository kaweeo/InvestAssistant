# Generated by Django 5.1.3 on 2024-11-29 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='avg_price',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
        migrations.AlterField(
            model_name='investment',
            name='total_quantity',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
    ]