from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
import random
import datetime

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(default='normal',max_length=20)
    account_number = models.CharField(
        null=True,
        max_length=20,
        validators=[RegexValidator(r'^\d+$', 'Account number must be a number')]
    )
    balance = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    currency = models.CharField(default='KES',max_length=3)
    transaction_history = models.JSONField(null=True,blank=True,)
    creation_date = models.DateField(default=datetime.datetime.now)
    status = models.CharField(max_length=20, default='active')
    address = models.CharField(null=True,blank=True,max_length=200)
    phone_number = models.CharField(null=True,blank=True,max_length=20)
    language = models.CharField(null=True,blank=True,max_length=20)
    time_zone = models.CharField(null=True,blank=True,max_length=40)
    
    billing_address = models.CharField(null=True,blank=True,max_length=200)
    payment_methods = models.JSONField(null=True,blank=True,)
    referral_code = models.CharField(null=True,blank=True,max_length=20)

    occupation = models.CharField(null=True,blank=True,max_length=100)
    income = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    credit_score = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    
    '''
    contact_preferences = models.JSONField(null=True)
    security_questions = models.JSONField(null=True)
    social_media_accounts = models.JSONField(null=True)
    notification_preferences = models.JSONField(null=True)
    bank_name = models.CharField(null=True,max_length=100)
    bank_routing_number = models.CharField(
        null=True,
        max_length=20,
        validators=[RegexValidator(r'^\d+$', 'Routing number must be a number')]
    )
    investment_portfolio = models.JSONField(null=True)
    insurance_coverage = models.JSONField(null=True)
    
    '''
   

    def __str__(self):
        return self.user.username
    
    def add_to_balance(self, amount):
        self.balance += amount
        self.save()
    
    def subtract_from_balance(self, amount):
        self.balance -= amount
        self.save()
    
    def generate_account_number(self):
        # Generate a random 10-digit number
        account_number = random.randint(1000000000, 9999999999)
        # Check if the number is already in use
        if Account.objects.filter(account_number=account_number).exists():
            # If it is, generate a new number
            return self.generate_account_number()
        # If it is not, return the number
        return account_number

    def add_transaction(self, amount, transaction_type, date):
        transaction = {
            'amount': amount,
            'transaction_type': transaction_type,
            'date': date
        }
        self.transaction_history.append(transaction)
        self.save()

    def transfer(self, recipient, amount, date):
        if not self.validate_transaction(amount):
            return 'Insufficient funds'
        self.subtract_from_balance(amount)
        recipient.add_to_balance(amount)
        self.add_transaction(amount, 'transfer', date)
        recipient.add_transaction(amount, 'transfer', date)

    def pay_bill(self, amount, bill):
        if self.balance < amount:
            return 'Insufficient funds'
        self.subtract_from_balance(amount)
        self.add_transaction(amount, f'bill payment ({bill})', datetime.now())

    def validate_transaction(self, amount):
        if self.balance < amount:
            return False
        return True

    def set_recurring_payment(self, recipient, amount, interval):
        # interval should be a string, e.g. 'weekly', 'monthly'
        payment = {
            'recipient': recipient,
            'amount': amount,
            'interval': interval
        }
        self.recurring_payments.append(payment)
        self.save()

    def cancel_recurring_payment(self, payment_id):
        for payment in self.recurring_payments:
            if payment['id'] == payment_id:
                self.recurring_payments.remove(payment)
                self.save()
                return
        return 'Payment not found'

    def schedule_payment(self, recipient, amount, date):
        payment = {
            'recipient': recipient,
            'amount': amount,
            'date': date
        }
        self.scheduled_payments.append(payment)
        self.save()

    def cancel_scheduled_payment(self, payment_id):
        for payment in self.scheduled_payments:
            if payment['id'] == payment_id:
                self.scheduled_payments.remove(payment)
                self.save()
                return
        return 'Payment not found'

    def cancel_scheduled_payment(self, payment_id):
        for payment in self.scheduled_payments:
            if payment['id'] == payment_id:
                self.scheduled_payments.remove(payment)
                self.save()
                return
        return 'Payment not found'

    def generate_statement(self, start_date, end_date):
        statement = {
            'start_date': start_date,
            'end_date': end_date,
            'transactions': []
        }
        for transaction in self.transaction_history:
            if transaction['date'] >= start_date and transaction['date'] <= end_date:
                statement['transactions'].append(transaction)
        return statement
