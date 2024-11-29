# Generated by Django 5.1.3 on 2024-11-29 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_price_per_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=4, max_digits=14),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=14),
        ),
    ]