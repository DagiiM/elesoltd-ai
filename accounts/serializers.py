from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Account,Merchant,Biller, Transaction,Card
from authentication.models import User
from rest_framework import serializers
from decimal import Decimal
import datetime
from .modifiers import *

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    
    account_detail = serializers.HyperlinkedIdentityField(
        view_name='account-detail',
        lookup_field='pk'
    )
    card_list = serializers.HyperlinkedIdentityField(
        view_name='card-list',
        lookup_url_kwarg='account_pk',
    )

    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'balance', 'max_balance', 'status', 'currency', 'creation_date', 'user',
                  'account_detail','card_list']
        
        extra_kwargs = {
                'request': {'required': False, 'write_only': True},
            }
    
class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'account', 'name']
        
class UpdateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_type','status','balance','currency']
        read_only_fields = ['account_type','status','balance','currency']

    def update(self, instance, validated_data):
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    customer = UserSerializer(read_only=True)
    beneficiary = UserSerializer(read_only=True)
    created_at = SanitizedDateTimeField()

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'payment_method', 'amount', 'description', 'reference_number', 'created_at','account', 'customer', 'beneficiary']
        depth = 1

class DepositSerializer(serializers.HyperlinkedModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    description = serializers.CharField(max_length=200)
    
    class Meta:
        model = Account
        fields = ['amount','description']

    def create(self, validated_data):
        account = self.context['account']
        amount = validated_data['amount']
        description = validated_data['description']
        try:
            transaction = account.deposit(amount=amount, description=description)
        except ValueError as err:
            raise ValueError(err.message)
        return transaction

      
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'errors': exc.detail,}, code='invalid')

    
class TransferSerializer(serializers.Serializer):
    beneficiary = serializers.CharField(max_length=30)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(max_length=200)
 
    def create(self, validated_data):
        source_account = self.context['source_account']
        beneficiary_account = validated_data['beneficiary']
        amount = validated_data['amount']
        description = validated_data['description']
        try:
            beneficiary = Account.objects.get(account_number=beneficiary_account).user
        except Account.DoesNotExist as e:
            raise serializers.ValidationError({"errors":f"The Account '{beneficiary_account}' does not exist"}) 
        try: 
            transaction = source_account.transfer(beneficiary=beneficiary,amount=amount, description=description)
        except ValueError as err:
            raise serializers.ValueError({'errors':err.message})
        return transaction      
        
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'errors': exc.detail,}, code='invalid')

    
    
class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=200)

    def create(self, validated_data):
        account = self.context['account']
        amount = validated_data['amount']
        description = validated_data['description']

        try:
            transaction = account.withdraw(amount=amount, description=description)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction


class BuyGoodsSerializer(serializers.Serializer):
    till_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(max_length=200)
    
    def validate_till_number(self, value):
        try:
            merchant = Merchant.objects.get(till_number=value)
        except Merchant.DoesNotExist:
            raise serializers.ValidationError("Merchant does not exist.")
        return merchant

  
    def create(self, validated_data):
        merchant = validated_data['till_number']
        amount = validated_data['amount']
        description = validated_data['description']
        account = self.context['account']
        try:
            transaction = account.buy_goods(merchant, amount, description)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction
    
class PayBillSerializer(serializers.Serializer):
    biller_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(max_length=200)
    
    def validate_biller_number(self, value):
        try:
            biller = Biller.objects.get(biller_number=value)
        except Biller.DoesNotExist:
            raise serializers.ValidationError("Biller does not exist.")
        return biller

  
    def create(self, validated_data):
        biller = validated_data['biller_number']
        amount = validated_data['amount']
        description = validated_data['description']
        account = self.context['account']
        try:
            transaction = account.pay_bill(biller, amount, description)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction
    
    
class CardSerializer(serializers.HyperlinkedModelSerializer):
    card_number = CardNumberField(max_length=16,read_only=True)
    expiration_date = ExpirationDateField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    #card_detail = serializers.HyperlinkedIdentityField(view_name='card-detail',lookup_url_kwarg='pk')

    class Meta:
        model = Card
        fields = ['id', 'card_type','card_number','beneficiary','description','balance','cvv_code', 'expiration_date',
                  'balance', 'is_active',]
        read_only_fields = ['id','card_number', 'expiration_date',  'cvv_code',]

    def create(self, validated_data):
        account = self.context['account']
        card_type = validated_data['card_type']
        beneficiary = validated_data['beneficiary']
        description = validated_data['description']
        balance = validated_data['balance']
        
        try:
            card = account.card.create_card(
                card_type=card_type,
                beneficiary=beneficiary,
                description=description,
                balance=balance
                )
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return card

    def update(self, instance, validated_data):
        instance.card_type = validated_data.get('card_type', instance.card_type)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'errors': exc.detail,}, code='invalid')

class CardDepositSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=1.00)
    
    class Meta:
        model = Account
        fields = ['amount']

    def create(self, validated_data):
        card = self.context['card']
        amount = validated_data['amount']
        try:
            transaction = card.card_deposit(amount=amount)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction

      
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({'errors': exc.detail,}, code='invalid')

class CardRedeemSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=7, decimal_places=2)
    card_number = CardNumberField(max_length=16)
    cvv_code = serializers.CharField(max_length=3)
    order_id = serializers.CharField()

    def validate_amount(self, value):
        if not isinstance(value, Decimal) or value <= Decimal('0'):
            raise serializers.ValidationError("Invalid amount.")
        return value

    def validate(self, data):
        card = self.context['card']
        card_number = data.get('card_number')
        cvv_code = data.get('cvv_code')

        try:
            card = Card.objects.get(cvv_code=cvv_code, card_number=card_number)
        except Card.DoesNotExist:
            raise serializers.ValidationError("Invalid virtual card information.")

        data['card'] = card
        return data
    
    
    def create(self, validated_data):
        card = self.context['card']
        order_id = validated_data['order_id']
        card_number = validated_data['card_number']
        amount = validated_data['amount']
        cvv_code = validated_data['cvv_code']
        try:
            transaction = card.card_redeem(
                order_id=order_id,
                amount=amount,
                card_number=card_number,
                cvv_code=cvv_code
                )
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction


class CardRefundSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if not isinstance(value, Decimal) or value <= Decimal('0'):
            raise serializers.ValidationError("Invalid amount.")
        return value

    def validate(self, data):
        card = self.context['card']

        if data['amount'] > card.balance:
            raise serializers.ValidationError("Refund amount exceeds card balance.")

        return data
    
    def create(self, validated_data):
        card = self.context['card']
        amount = validated_data['amount']
        try:
            transaction = card.card_refund(amount=amount)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction

class CardTransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    card_number = CardNumberField(max_length=16)

    def validate_card_number(self, value):
        # Check if the card exists and is not the same as the source card
        card = Card.objects.filter(card_number=value).first()
        if not card:
            raise serializers.ValidationError("Invalid destination card.")
        if card == self.context['card']:
            raise serializers.ValidationError("Cannot transfer funds to the same card.")
        return card

    def validate_amount(self, value):
        # Check if the amount is positive and less than or equal to the source card's balance
        if value <= 0:
            raise serializers.ValidationError("Transfer amount must be a positive number.")
        if value > self.context['card'].balance:
            raise serializers.ValidationError("Insufficient funds to cover transfer.")
        return value

    def validate(self, data):
        # Add fee to the data
        data['fee'] = Decimal('0.50') # or any fee calculation logic
        return data
        
    def create(self, validated_data):
        card = self.context['card']
        card_number = validated_data['card_number']
        amount =  validated_data['amount']
        try:
            transaction = card.card_transfer(amount=amount,to_card=card_number)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction
    
class DeactivateCardSerializer(serializers.Serializer):
    card_number = CardNumberField(max_length=16)
    """
    Serializer for deactivating a card.
    """
    class Meta:
        fields = ['card_number']
        
    def create(self, validated_data):
        card = self.context['card']
        card_number = validated_data['card_number']
        try:
            transaction = card.card_deactivate(card_number=card_number)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return transaction
    
    