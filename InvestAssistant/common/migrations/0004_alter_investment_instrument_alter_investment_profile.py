# Generated by Django 5.1.3 on 2024-12-09 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_options_profile_balance'),
        ('common', '0003_alter_investment_avg_price_and_more'),
        ('instruments', '0005_alter_instrument_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instruments', to='instruments.instrument'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='accounts.profile'),
        ),
    ]