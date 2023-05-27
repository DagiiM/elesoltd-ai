from decimal import Decimal
from django.db import models, transaction
from authentication.models import User
from django.core.validators import RegexValidator
from notifications.utils import send_activation_email
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime, random,uuid
from django.core.exceptions import ValidationError
from typing import Optional
from django.utils import timezone
from uuid import uuid4
from datetime import date
import string,re
from django.utils.translation import gettext_lazy as _
from django.db.models import F,Value
from django.core.validators import MinValueValidator, MaxValueValidator
import logging
from django.db.utils import OperationalError
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import CombinedExpression

logger = logging.getLogger(__name__)

class AccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='active')
    
    def get_by_natural_key(self, account_number):
        return self.get(account_number=account_number)


class Account(models.Model):
    """
    Model representing a bank account.
    """
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]
    ACCOUNT_TYPES_INDIVIDUAL = 'Individual Account'
    ACCOUNT_TYPES_BUSINESS = 'Business Account'
    ACCOUNT_TYPES = [
        (ACCOUNT_TYPES_INDIVIDUAL, 'Individual Account'),
        (ACCOUNT_TYPES_BUSINESS, 'Business Account'),
    ]
    CURRENCY_KES = 'KES'
    CURRENCY_USD = 'USD'
    CURRENCY_EUR = 'EUR'
    CURRENCY_CHOICES = [
        (CURRENCY_KES, 'Kenyan Shilling'),
        (CURRENCY_USD, 'US Dollar'),
        (CURRENCY_EUR, 'Euro'),
    ]

    #user = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,unique=True, on_delete=models.CASCADE, related_name='account', editable=False)
    account_type = models.CharField(choices=ACCOUNT_TYPES, default=ACCOUNT_TYPES_INDIVIDUAL, max_length=20)
    account_number = models.CharField(
        #primary_key=True,
        unique=True,
        max_length=15,
        editable=False,
        validators=[RegexValidator(r'^\d+$', 'Account number must be a number')]
    )
    #balance = models.DecimalField(decimal_places=2,max_digits=9,default=Decimal('0.00'))
    #max_balance = models.DecimalField(decimal_places=2,max_digits=9,default=Decimal('9999999.00'))
    balance = models.DecimalField(decimal_places=2,max_digits=9,default=Decimal('0.00'), validators=[MinValueValidator(0)])
    max_balance = models.DecimalField(decimal_places=2,max_digits=9,default=Decimal('9999999.00'), validators=[MinValueValidator(0), MaxValueValidator(9999999)])

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE,verbose_name='Status')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=CURRENCY_KES)
    creation_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'accounts'

    def __str__(self):
        return self.account_number

    @transaction.atomic
    def deposit(self:'Account', amount: Decimal, balance_field: str = 'balance', description: Optional[str] = None, persist: Optional[str] = None) -> None:
        """
        Deposits the specified amount into the account.

        Args:
            amount (Decimal): The amount to deposit.
            balance_field (str): The name of the attribute to use for the account balance. Default is 'balance'.
            persist (callable): A function to call to persist the changes made to the account. Default is None.
        """
        self.validate_deposit(amount=amount)

        setattr(self, balance_field, getattr(self, balance_field) + amount)
        self.save()

        if persist is not None:
            persist(self)

        transaction = self.create_transaction(amount=amount, transaction_type=Transaction.DEPOSIT, description=description)

        return transaction

    @transaction.atomic
    def withdraw(self:'Account', amount: Decimal, description: Optional[str] = None) -> 'Transaction':
        """
        Withdraws the specified amount from this account.

        Parameters:
        amount (Decimal): The amount to withdraw.
        description (str, optional): A description of the withdrawal. Defaults to None.

        Returns:
        Transaction: The newly created transaction object, representing the withdrawal.

        Raises:
        ValueError: If the amount is less than or equal to zero, or if the account balance is insufficient to cover the withdrawal.
        """
        self.validate_withdrawal(amount)

        self.balance -= amount
        self.save()
        withdrawal_transaction = self.create_transaction(amount=amount, transaction_type=Transaction.WITHDRAWAL, description=description)

        return withdrawal_transaction

    @transaction.atomic
    def transfer(self:'Account', beneficiary: 'User', amount: Decimal, description: Optional[str] = None) -> 'Transaction':
        """
        Transfers the specified amount from this account to another account.

        Parameters:
        beneficiary (User): The beneficiary user object.
        amount (Decimal): The amount to transfer.
        description (str, optional): A description of the transfer. Defaults to None.

        Returns:
        Tuple[Transaction, Transaction]: A tuple of the newly created transaction objects, representing the outgoing and incoming transfers, respectively.
        
        Raises:
        ValueError: If the amount is less than or equal to zero, or if the account balance is insufficient to cover the transfer, or if the beneficiary account does not exist, or if the beneficiary account belongs to the same user.
        """
        destination_account = str(beneficiary.account.account_number)
        beneficiary_account=Account.validate_transfer(self, beneficiary=destination_account, amount=amount, description=description)
        
        self.balance -= amount
        beneficiary_account.balance += amount
        self.save()
        beneficiary_account.save()
        transfer_out_transaction = self.create_transaction(amount=amount, transaction_type=Transaction.TRANSFER_OUT, description=description)
        transfer_in_transaction = beneficiary_account.create_transaction(amount=amount, transaction_type=Transaction.TRANSFER_IN, description=description)

        return transfer_out_transaction
    
    def buy_goods(self:'Account', merchant: 'Merchant', amount: Decimal, description: Optional[str] = None) -> 'Transaction':
    
        try:
            transfer_cash = self.transfer(beneficiary=merchant.account.user, amount=amount, description=description)
        except ValueError as e:
            raise ValueError(str(e))
        return transfer_cash

    def pay_bill(self:'Account', biller: 'Biller', amount: Decimal, description: Optional[str] = None) -> 'Transaction':
        try:
            transfer_cash = self.transfer(beneficiary=biller.account.user, amount=amount, description=description)
        except ValueError as e:
            raise ValueError(str(e))
        return transfer_cash

    def mini_statement(self:'Account', no_of_transactions:Optional[int]=15) -> 'Transaction':
        transactions = Transaction.objects.filter(account=self).order_by('-created_at')[:no_of_transactions]
        return transactions

    def generate_statement(self:'Account', num_transactions:Optional[int]=100, start_date:Optional[date] = None, end_date:Optional[date] = None) -> 'Transaction':
        transactions = self.transactions.all()
        if start_date and end_date:
            transactions = transactions.filter(date__range=(start_date, end_date))
        transactions = transactions.order_by('-created_at')[:num_transactions]
        return transactions
    
    def validate_amount(self:'Account',amount: Decimal) -> None:
        """
        Validates whether the specified amount is valid.

        Args:
            amount (Decimal): The amount to validate.

        Raises:
            ValidationError: If the amount is not positive.
        """
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        
    def validate_min_balance(self: 'Account',amount: Decimal) -> None:
        """
        Validates whether the specified balance is sufficient to cover the specified amount.

        Args:
            balance (Decimal): The current account balance.
            amount (Decimal): The amount to validate.

        Raises:
            ValidationError: If the balance is insufficient to cover the amount.
        """
        if self.balance < amount:
            raise ValidationError("Your Balance is Insufficient")
        
    def validate_max_balance(self:'Account',amount:Decimal):
        if self.balance + amount > self.max_balance:
            raise ValidationError(f"Target Account Can't credit {amount} without Exceeding Maximum Balance.")
        
    def validate_transfer(self: 'Account', beneficiary: str, amount: Decimal, description: str) -> 'Account':
        """
        Validates whether the specified transfer amount is valid.

        Args:
            self (Account): The source account for the transfer.
            beneficiary (str): The account number of the destination account.
            amount (Decimal): The amount to transfer.
            description (str): A description of the transfer.

        Raises:
            ValidationError: If the amount is not positive, if the source account has insufficient balance, if the destination account does not exist, if the destination account belongs to the same user as the source account, or if the transfer amount would exceed the maximum account balance of the destination account.

        Returns:
            Account: The destination account.
        """
        self.validate_amount(amount=amount)
        self.validate_min_balance(amount)

        if self.account_number == beneficiary:
            raise ValidationError('Cannot transfer to own account.')
       
        try:
            destination_account = Account.objects.select_for_update().get(account_number=beneficiary)
        except self.DoesNotExist:
            raise ValidationError('Beneficiary account does not exist.')
            
        if destination_account.user == self.user:
            raise ValidationError('Cannot transfer to own account.')

        destination_account.validate_max_balance(amount)

        return destination_account
        
    def validate_deposit(self:'Account',amount: Decimal) -> None:
        """
        Validates whether the specified deposit amount is valid.

        Args:
            amount (Decimal): The amount to deposit.
            balance (Decimal): The current account balance.
            max_balance (Decimal): The maximum account balance allowed.

        Raises:
            ValidationError: If the deposit amount is not positive or if it would exceed the maximum account balance.
        """
        
        self.validate_amount(amount=amount)
        self.validate_max_balance(amount)

    def validate_withdrawal(self:'Account',amount: Decimal) -> None:
        """
        Validates whether the specified withdrawal amount is valid.

        Args:
            amount (Decimal): The amount to withdraw.
            balance (Decimal): The current account balance.

        Raises:
            ValidationError: If the withdrawal amount is not positive or if it exceeds the account balance.
        """
        self.validate_amount(amount=amount)
        self.validate_min_balance(amount)
 
        
    @staticmethod
    def generate_reference_number():
        reference_number = str(uuid.uuid4())[:8].upper()
        while Transaction.objects.filter(reference_number=reference_number).exists():
            reference_number = str(uuid.uuid4())[:8].upper()
        return reference_number
    
    def create_transaction(self:'Account', amount: Decimal, transaction_type,payment_method:Optional[str]=None, description: Optional[str]=None) -> 'Transaction':
        """
        Creates a new transaction for this account.

        Parameters:
        amount (float): The amount of the transaction.
        transaction_type (str): The type of the transaction, one of the constants defined in the Transaction class.
        description (str, optional): A description of the transaction. Defaults to None.
        beneficiary (Account, optional): The account that is the beneficiary of the transaction. Only used for transfer transactions. Defaults to None.

        Returns:
        Transaction: The newly created transaction object.
        """
        transaction = Transaction.objects.create(
            account=self,
            payment_method=payment_method or 'INTERNAL',
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            reference_number=self.generate_reference_number(),
        )
        return transaction
    
    @staticmethod
    def generate_number(model_class, field_name, start_number):
        last_number = model_class.objects.order_by(f'-{field_name}').values_list(field_name, flat=True).first()
        if last_number is None:
            # This is the first record, start at the given start number
            return start_number
        else:
            # Increment the last number and return the new number
            return str(int(last_number) + 1)
    
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = Account.generate_number(Account, 'account_number', '10000000000')
        super().save(*args, **kwargs)
        
    @receiver(post_save, sender=User)
    def create_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
            send_activation_email(user=instance,email=instance.email) # Sent when a user is created
            


class Transaction(models.Model):
    DEPOSIT = 'D'
    WITHDRAWAL = 'W'
    TRANSFER_IN = 'TI'
    TRANSFER_OUT = 'TO'
    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER_IN, 'Transfer In'),
        (TRANSFER_OUT, 'Transfer Out'),
    ]
    PAYMENT_INTERNAL = 'INTERNAL'
    PAYMENT_MPESA = 'MPESA'
    PAYMENT_PAYPAL = 'PAYPAL'
    PAYMENT_CREDIT_CARD = 'CREDIT_CARD'
    PAYMENT_DEBIT_CARD = 'DEBIT_CARD'
    PAYMENT_BANK_TRANSFER = 'BANK_TRANSFER'
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_INTERNAL, 'Internal Payment'),
        (PAYMENT_MPESA, 'M-PESA'),
        (PAYMENT_PAYPAL, 'PayPal'),
        (PAYMENT_CREDIT_CARD, 'Credit Card'),
        (PAYMENT_DEBIT_CARD, 'Debit Card'),
        (PAYMENT_BANK_TRANSFER, 'Bank Transfer'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        help_text='Transaction type describing movement of money from an Account.'
        )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_INTERNAL,
        help_text='The payment method used for this payment.'
    )
    amount = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal('0.00'))
    _description = models.TextField(
        blank=False,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9\-\_\.\,\:\;\!\?\s]+$',
            message='Description can only contain letters, digits, spaces and some punctuation marks'
        )]
        )
    reference_number = models.CharField(max_length=8, unique=True, primary_key=True)
    date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_description(self):
        return self._description
    def set_description(self, description):
        self._description = description.casefold()
        
    description = property(get_description, set_description)
    
    def __str__(self):
        return self.reference_number
    
    
class CommonFields(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
        
    def can_edit_name(self):
        window = timezone.timedelta(days=30)  # set the window to 30 days
        return timezone.now() < (self.created_at + window)
        
class Biller(CommonFields):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    biller_number = models.CharField(
        unique=True,
        max_length=20,
        editable=False,
        validators=[RegexValidator(r'^\d+$', 'Biller number must be a number')]
    )
    
    def __str__(self):
        return f"{self.biller_number} - {self.name} ({self.phone}, {self.email})"

    def save(self, *args, **kwargs):
        if not self.biller_number:
            self.biller_number = Account.generate_number(Biller, 'biller_number', '200000')
        super().save(*args, **kwargs)


class Merchant(CommonFields):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    till_number = models.CharField(
        unique=True,
        max_length=20,
        editable=False,
        validators=[RegexValidator(r'^\d+$', 'Till number must be a number')]
    )

    def __str__(self):
        return f"{self.till_number} - {self.name}"
        

    def save(self, *args, **kwargs):
        if not self.till_number:
            self.till_number = Account.generate_number(Merchant, 'till_number', '400000')
        super().save(*args, **kwargs)


    @staticmethod
    def is_email_unique(email):
        """
        Checks if an email is unique.

        Args:
        email (str): The email to check.

        Returns:
        bool: True if the email is unique, False otherwise.
        """
        return not Merchant.objects.filter(email=email).exists()

class MyCardManager(models.Manager):
    def create_card(self:'Account', card_type, balance:Decimal, beneficiary:str,description:str):
        try:
            if beneficiary.isalpha():
                raise ValidationError("Beneficiary name can only contain letters")
            card_number = Card.generate_card_number()
            cvv_code = Card.generate_cvv_code()
            card = self.create(
                card_type=card_type,
                card_number=card_number,
                cvv_code=cvv_code,
                beneficiary=beneficiary,
                description=description
                )

            card.save()
            card.card_deposit(amount=balance)
            return card
        except InsufficientFundsError:
            raise ValidationError('Insufficient Wallet Balance')
        '''
    def update_card_balance(self:'Card',instance):
        if instance.balance != instance.old_balance:
            try:
                self.card_balance_update(instance)
            except InsufficientFundsError:
                instance.balance = instance.old_balance
                self.save()
                raise ValidationError('Insufficient Wallet Balance')
            
                
    def update(self, instance, validated_data):
        old_balance = instance.balance if instance.pk else None
        instance = super().update(instance, validated_data)
        self.update_card_balance(instance, old_balance)
        return instance
    
    def card_balance_update(self, instance):
        amount = instance.old_balance - instance.balance
        if instance.old_balance > instance.balance:
            instance.card_refund(amount=amount)
        elif instance.old_balance < instance.balance:
            instance.card_deposit(amount=abs(amount))

        '''
        
class Card(models.Model):
    CARD_TYPES = (
        ('VISA', 'Visa'),
        ('MC', 'Mastercard'),
        ('AMEX', 'American Express'),
        ('DISC', 'Discover'),
    )

    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='card',verbose_name=_('account'))
    card_number = models.CharField(max_length=16, validators=[RegexValidator(r'^\d+$', 'Card number must be a number')], unique=True,editable=False,)
    cvv_code = models.CharField(max_length=3, null=True, validators=[RegexValidator(r'^\d+$', 'Cvv code must be a number')],editable=False)
    card_type = models.CharField(max_length=25,choices=CARD_TYPES,)
    beneficiary = models.CharField(max_length=100,blank=False)
    description = models.TextField(
        blank=False,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9\-\_\.\,\:\;\!\?\s]+$',
            message='Description can only contain letters, digits, spaces and some punctuation marks'
        )]
        )
    expiration_date = models.DateField(default=timezone.now() + timezone.timedelta(days=30),editable=False)
    balance = models.DecimalField(decimal_places=2,max_digits=9,default=Decimal('0.00'), validators=[MinValueValidator(0)])
    old_balance = models.DecimalField(decimal_places=2,max_digits=9,default=Decimal('0.00'), validators=[MinValueValidator(0)])
    min_balance = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.01'),validators=[MinValueValidator(0)],editable=False)
    max_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('10000.00'),validators=[MinValueValidator(0), MaxValueValidator(9999)],editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = MyCardManager()
    
    def get_masked_card_number(self):
        return f"{self.card_number[:4]} **** **** {self.card_number[-4:]}"

    def set_masked_card_number(self, value):
        raise AttributeError("Masked card number cannot be set.")
    
    masked_card_number = property(get_masked_card_number, set_masked_card_number)

    
    def __str__(self):
        return f"owner: {self.account.user.first_name} {self.account.user.last_name}, beneficiary : {self.beneficiary}"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_balance = self.balance
    
    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self.generate_card_number()
        if not self.cvv_code:
            self.cvv_code = self.generate_cvv_code()
                
        if not self.pk:  # if the instance is being created
            try:
                self.validate_card(self.card_number, self.cvv_code)
                self.harmonize_card_balance_with_account()
            except ValueError as error:
                raise ValidationError(str(error))
            super().save(*args, **kwargs)
         
        else:  # if the instance is being updated
            card = Card.objects.get(pk=self.pk)                
            if (self.card_number != card.card_number or
                    self.cvv_code != card.cvv_code or
                    self.balance != card.balance):
                try:
                    self.validate_card(self.card_number, self.cvv_code)
                except ValueError as error:
                    raise ValidationError(str(error))
                #Card.objects.update_card_balance(self)
            super().save(*args, **kwargs)
        
    @staticmethod
    def generate_card_number():
        numbers = string.digits
        card_number = ''.join(random.choice(numbers) for i in range(16))
        return card_number
        
    @staticmethod    
    def generate_cvv_code():
        numbers = string.digits
        cvv_code = ''.join(random.choice(numbers) for i in range(3))
        return cvv_code
    
    @transaction.atomic        
    def card_deposit(self:'Card', amount:Decimal):
        if not isinstance(amount, Decimal) or amount <= 0:
            raise ValueError("Deposit amount must be a positive decimal number.")
        if self.balance + amount > self.max_balance:
            raise ValueError("Deposit amount exceeds maximum balance.")
        
        self.validate_card(self.card_number, self.cvv_code)
        
        self.account.withdraw(amount=amount,description=f'Funds drawn from your account - {self.account.currency}. {amount}')

        self.balance = F('balance') + amount
        self.old_balance = self.balance
        self.save(update_fields=['balance','old_balance'])
        
        transaction = self.account.create_transaction(
            transaction_type='deposit',
            payment_method='internal',
            amount=amount,
            description=f"Deposit to gift card {self.masked_card_number}",
        )
        transaction.save()
        
        return transaction
    
    @transaction.atomic
    def card_redeem(self:'Card', order_id: str, amount: Decimal, card_number: str, cvv_code: str):
        self.validate_card_redeem(order_id, amount, card_number, cvv_code)
        
        self.balance = F('balance') - amount
        self.old_balance = self.balance
        self.save(update_fields=['balance','old_balance'])

        transaction = self.account.create_transaction(
            transaction_type='card redeem',
            payment_method='gift_card',
            amount=amount,
            description=f"Redeem from gift card {self.masked_card_number} for order {order_id}",
        )

        transaction.save()
        
        return transaction
            
    @transaction.atomic()   
    def card_refund(self:'Card', amount:Decimal):
        self.validate_card(self.card_number, self.cvv_code)
        account = self.account.deposit(
            amount=amount,
            description=f'{self.account.currency} {amount}, Refunded from Virtual Card - {self.masked_card_number}'
            )
        self.balance = F('balance') - amount
        self.old_balance = self.balance
        self.save(update_fields=['balance','old_balance'])
        
        transaction = self.account.create_transaction(
            transaction_type='card refund',
            payment_method='Card to Account Transfer',
            amount=amount,
            description=f"Refund from gift card - {self.masked_card_number}",
        )
        transaction.save()
        return transaction

    def card_deactivate(self:'Card',card_number:str):
        self.validate_card(card_number, self.cvv_code)
        self.is_active = False
        self.save(update_fields=['is_active'])
        return self

    def validate_card_redeem(self, order_id, amount, card_number, cvv_code):
        if not order_id or order_id.isspace():
            raise ValueError("Invalid order ID.")
        
        if not isinstance(amount, Decimal) or amount <= Decimal('0'):
            raise ValueError("Invalid amount.")
        
        self.validate_card(card_number, cvv_code)

        if self.balance < amount:
            raise ValueError("Insufficient balance.")

        if self.balance - amount < self.min_balance:
            raise ValueError("Redeem amount would result in balance below minimum balance.")
        

    def validate_card(self, card_number, cvv_code):
        if card_number != self.card_number or cvv_code != self.cvv_code:
            raise ValueError("Invalid virtual card information.")
        
        if not self.is_active:
            raise ValueError("Gift card is not active.")
        '''
        if self.expiration_date and (self.expiration_date or self.expiration_date()) < datetime.date.today():
            raise ValueError("Gift card has expired.")
        '''
        
    def card_transfer(self, amount: Decimal, to_card: Optional['Card'] = None, fee: Decimal = Decimal(0)):
        """
        Transfer funds from one card to another
        :param amount: the amount of funds to be transferred
        :param to_card: the card to which the funds are being transferred
        :param fee: the fee to be deducted from the transfer amount
        """
        if not isinstance(amount, Decimal) or amount <= 0:
            raise ValueError("Transfer amount must be a positive decimal number.")
        if amount > self.max_balance - self.balance:
            raise ValueError("Transfer amount exceeds maximum balance.")
        if not to_card:
            raise ValueError("Destination card must be specified for a transfer.")
        if not isinstance(to_card, Card):
            raise ValueError("Destination card must be a valid Card instance.")
        if to_card == self:
            raise ValueError("Cannot transfer funds to the same card.")
        if amount + fee > self.balance:
            raise ValueError("Insufficient funds to cover transfer and fee.")

        with transaction.atomic():
            self.card_refund(amount=amount + fee)
            to_card.card_deposit(amount=amount)

            transfer_description = f"{amount} transferred from card {self.masked_card_number} to card {to_card.masked_card_number}"
            transaction_out = self.account.create_transaction(
                transaction_type='card transfer outgoing',
                payment_method='internal',
                amount=amount + fee,
                description=transfer_description
            )
            to_card.account.create_transaction(
                transaction_type='card transfer incoming',
                payment_method='internal',
                amount=amount,
                description=transfer_description
            )

            if fee > 0:
                self.account.create_transaction(
                    transaction_type='fee outgoing',
                    payment_method='internal',
                    amount=fee,
                    description=f"Transfer fee for {transfer_description}"
                )
                to_card.account.create_transaction(
                    transaction_type='fee incoming',
                    payment_method='internal',
                    amount=fee,
                    description=f"Transfer fee for {transfer_description}",
                )
            return transaction_out
        
    def harmonize_card_balance_with_account(self:'Card'):
        """
        Transfers funds between a card and its associated account to match their balance.

        Parameters:
        - self: a Card object with a 'balance' and 'old_balance' attribute, and an 'account' attribute representing its associated account.
        - account: an Account object that is associated with the card.

        Returns: None
        
        Note: The 'balance' attribute of the 'Card' object is updated implicitly
            by the 'deposit' and 'withdraw' methods of the 'Account' object.
        
        """
        balance_diff = abs(self.balance - self.old_balance)
        if self.old_balance > self.balance:
            self.account.deposit(amount=balance_diff, description=f"Deposit to account from card {self.masked_card_number}")
            self.old_balance = self.balance
        elif self.balance > self.old_balance:
            self.account.withdraw(amount=balance_diff, description=f"Draw from account to card {self.masked_card_number}")
            self.old_balance = self.balance
    


class TransferError(Exception):
    pass
        
class InsufficientFundsError(Exception):
    pass

class SchemeCodeError(Exception):
    pass

class TransactionCodeError(Exception):
    pass