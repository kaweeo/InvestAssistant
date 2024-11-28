# Generated by Django 5.1.3 on 2024-11-28 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the investment instrument (e.g., Apple, Bitcoin, Vanguard ETF).', max_length=100)),
                ('ticker', models.CharField(help_text='The unique ticker symbol of the instrument.', max_length=10, unique=True)),
                ('current_price', models.DecimalField(decimal_places=2, help_text='The current market price per unit of the instrument.', max_digits=10)),
                ('type', models.CharField(choices=[('SECURITY', 'Security'), ('ETF', 'ETF'), ('REAL_ESTATE', 'Real Estate'), ('CRYPTO', 'Crypto Currency')], help_text='The sector or type of instrument (e.g., Security, ETF, Real Estate, Crypto).', max_length=20)),
            ],
            options={
                'verbose_name': 'Instrument',
                'verbose_name_plural': 'Instruments',
                'ordering': ['name'],
            },
        ),
    ]
