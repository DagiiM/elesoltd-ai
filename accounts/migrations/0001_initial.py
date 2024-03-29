# Generated by Django 4.1.7 on 2023-03-19 16:12

import datetime
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('normal', 'Normal'), ('savings', 'Savings')], default='normal', max_length=20)),
                ('account_number', models.CharField(editable=False, max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Account number must be a number')])),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=9)),
                ('max_balance', models.DecimalField(decimal_places=2, default=Decimal('9999999.00'), max_digits=9)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20, verbose_name='Status')),
                ('currency', models.CharField(choices=[('KES', 'Kenyan Shilling'), ('USD', 'US Dollar'), ('EUR', 'Euro')], default='KES', max_length=3)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='CommonFields',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('address', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_type', models.CharField(choices=[('D', 'Deposit'), ('W', 'Withdrawal'), ('TI', 'Transfer In'), ('TO', 'Transfer Out')], help_text='Transaction type describing movement of money from an Account.', max_length=10)),
                ('payment_method', models.CharField(choices=[('INTERNAL', 'Internal Payment'), ('MPESA', 'M-PESA'), ('PAYPAL', 'PayPal'), ('CREDIT_CARD', 'Credit Card'), ('DEBIT_CARD', 'Debit Card'), ('BANK_TRANSFER', 'Bank Transfer')], default='INTERNAL', help_text='The payment method used for this payment.', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('_description', models.TextField(validators=[django.core.validators.RegexValidator(message='Description can only contain letters, digits, spaces and some punctuation marks', regex='^[a-zA-Z0-9\\-\\_\\.\\,\\:\\;\\!\\?\\s]+$')])),
                ('reference_number', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(editable=False, max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Card number must be a number')])),
                ('cvv_code', models.CharField(editable=False, max_length=3, null=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Cvv code must be a number')])),
                ('card_type', models.CharField(choices=[('VISA', 'Visa'), ('MC', 'Mastercard'), ('AMEX', 'American Express'), ('DISC', 'Discover')], max_length=25)),
                ('beneficiary', models.CharField(max_length=100)),
                ('description', models.TextField(validators=[django.core.validators.RegexValidator(message='Description can only contain letters, digits, spaces and some punctuation marks', regex='^[a-zA-Z0-9\\-\\_\\.\\,\\:\\;\\!\\?\\s]+$')])),
                ('expiration_date', models.DateField(default=datetime.datetime(2023, 4, 18, 16, 12, 46, 662312, tzinfo=datetime.timezone.utc), editable=False)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6)),
                ('min_balance', models.DecimalField(decimal_places=2, default=Decimal('0.01'), editable=False, max_digits=10)),
                ('max_balance', models.DecimalField(decimal_places=2, default=Decimal('10000.00'), editable=False, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='accounts.account', verbose_name='account')),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('commonfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.commonfields')),
                ('till_number', models.CharField(editable=False, max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Till number must be a number')])),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            bases=('accounts.commonfields',),
        ),
        migrations.CreateModel(
            name='Biller',
            fields=[
                ('commonfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.commonfields')),
                ('biller_number', models.CharField(editable=False, max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Biller number must be a number')])),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            bases=('accounts.commonfields',),
        ),
    ]
