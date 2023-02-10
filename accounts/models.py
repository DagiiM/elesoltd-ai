from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import random
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.core.exceptions import ValidationError
import uuid

class AccountManager(models.Manager):
    def get_by_natural_key(self,account_number):
        return self.get(account_number=account_number)

class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    account_type = models.CharField(default='normal',max_length=20)
    account_number = models.CharField(
        primary_key=True,
        unique=True,
        max_length=20,
        validators=[RegexValidator(r'^\d+$', 'Account number must be a number')]
    )
    balance = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal('0.00'))
    max_balance = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal('9999999.00'))
    status = models.CharField(max_length=20, default='active')
    currency = models.CharField(default='KES',max_length=3)
    creation_date = models.DateField(default=datetime.datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = AccountManager()
 
    def __str__(self):
        return self.user.username
    
    def add_to_balance(self, amount):
        self.validate_transaction(amount)
        self.balance += amount
        self.save()
    
    def subtract_from_balance(self, amount):
        self.validate_transaction(amount)
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

    def transfer(self, beneficiary, amount):
        if self.balance - amount < 0:
            raise ValidationError("Insufficient funds to complete transaction.")
        if self == beneficiary:
            raise ValidationError("Can't transfer money to self.")
        self.subtract_from_balance(amount)
        beneficiary.add_to_balance(amount)
        beneficiary.save()

    def pay_bill(self, amount, bill):
        self.validate_transaction(amount)
        self.subtract_from_balance(amount)

    def validate_transaction(self, amount):
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        if self.balance + amount > self.max_balance:
            raise ValidationError("Transaction exceeds account's max balance")
        return True

    def mini_statement(self,no_of_transactions=15):
        transactions = Transaction.objects.filter(self).order_by('-date')[:no_of_transactions]
        return transactions

    def generate_statement(self, num_transactions=100, start_date=None, end_date=None):
        transactions = self.transactions.all()
        if start_date and end_date:
            transactions = transactions.filter(date__range=(start_date, end_date))
        transactions = transactions.order_by('-date')[:num_transactions]
        return transactions

    def save(self, *args, **kwargs):
        if not self.pk:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)
        
    @receiver(post_save, sender=User)
    def create_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
            
Account._meta.pk = Account._meta.get_field('account_number')

def generate_reference_number():
    reference_number = str(uuid.uuid4())[:8]
    while Transaction.objects.filter(reference_number=reference_number).exists():
        reference_number = str(uuid.uuid4())[:8]
    return reference_number

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('deposit','Deposit'),
        ('withdraw','Withdraw'),
        ('transfer','Transfer'),
    )    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    customer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='customer_transactions',related_query_name='customer_transaction')
    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE,related_name='beneficiary_transactions',related_query_name='beneficiary_transaction')

    transaction_type = models.CharField(max_length=10,choices=TRANSACTION_TYPE_CHOICES)
    payment_method = models.CharField(default='internal',max_length=20)
    amount = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal('0.00'))
    description = models.TextField(null=True,blank=True)
    reference_number = models.CharField(max_length=8, unique=True, default=generate_reference_number, primary_key=True)
   # status = models.BooleanField(default=True)
    date = models.DateField(default=datetime.datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    '''
    charge_id = models.CharField(max_length=100)
    discount_rate = models.FloatField()
    tax_rate = models.FloatField()
    refunded = models.FloatField()
    '''
    
@receiver(post_save,sender=Transaction)
def update_account_balance(sender,instance,**kwargs):
    account = instance.account
    if instance.transaction_type == 'deposit':
        account.add_to_balance(instance.amount)
    elif instance.transaction_type == 'transfer':
        customer = instance.customer.account_set.get()
        customer.transfer(account,instance.amount)
    elif instance.transaction_type == 'withdraw':
        if account.balance < instance.amount:
            return 'Insufficient funds'
        else:
            account.substract_from_balance(instance.amount)
    account.save()


    