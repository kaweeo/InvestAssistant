# Generated by Django 5.1.3 on 2024-12-09 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_price_per_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=4, max_digits=14),
        ),
    ]
