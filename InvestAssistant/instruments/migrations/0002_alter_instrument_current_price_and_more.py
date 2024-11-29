# Generated by Django 5.1.3 on 2024-11-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='current_price',
            field=models.FloatField(help_text='The current market price per unit of the instrument.'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='ticker',
            field=models.CharField(blank=True, help_text='The unique ticker symbol of the instrument.', max_length=10, null=True, unique=True),
        ),
    ]