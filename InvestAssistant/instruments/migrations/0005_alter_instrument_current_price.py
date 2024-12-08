# Generated by Django 5.1.3 on 2024-12-07 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0004_alter_instrument_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='current_price',
            field=models.DecimalField(decimal_places=4, default=0.0, help_text='The current market price per unit of the instrument.', max_digits=14),
        ),
    ]
