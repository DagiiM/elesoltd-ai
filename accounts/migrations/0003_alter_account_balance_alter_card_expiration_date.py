# Generated by Django 4.1.7 on 2023-03-20 10:11

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_card_old_balance_alter_card_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=9, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 19, 10, 11, 16, 159813, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
