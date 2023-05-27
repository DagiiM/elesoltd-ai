from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .models import Account,Card
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .modifiers import handle_validation_error

from .serializers import (
    AccountSerializer,
    UpdateAccountSerializer,
    TransactionSerializer,
    DepositSerializer,
    TransferSerializer,
    WithdrawalSerializer,
    BuyGoodsSerializer,
    PayBillSerializer,
    CardSerializer,
    CardRedeemSerializer,
    CardRefundSerializer,
    CardTransferSerializer,
    DeactivateCardSerializer,
    CardDepositSerializer
    )

class ReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    def get_allowed_methods(self):
        methods = super().get_allowed_methods()
        #methods.remove('get','update','destroy')
        return methods
    
class AccountViewSet(ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.order_by('-creation_date')
    
    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateAccountSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        account = self.get_object()
        return Response({'balance': account.balance})

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        account = self.get_object()
        serializer = DepositSerializer(data=request.data,context={'account': account})
        serializer.is_valid(raise_exception=True)
        try:
            transaction = serializer.save()
        except ValidationError as e:
            return handle_validation_error(e)
        return self.success_response(request, transaction,message='Funds Deposit successful')


    @action(detail=True, methods=['post'])
    def withdrawal(self, request, pk=None):
        account = self.get_object()
        serializer = WithdrawalSerializer(data=request.data,context={'account': account})
        serializer.is_valid(raise_exception=True)
        try:
            transaction = serializer.save()
        except ValidationError as e:
            return handle_validation_error(e)
        return self.success_response(request, transaction,message='Funds withdrawal successful')
    
    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        source_account = self.get_object()
        serializer = TransferSerializer(data=request.data, context={'source_account': source_account})
        serializer.is_valid(raise_exception=True)
        try:
            transaction = serializer.save()
        except ValidationError as e:
            return handle_validation_error(e)
        return self.success_response(request, transaction,message='Funds transfer successful')
    
    @action(detail=True, methods=['post'])
    def buy_goods(self, request, pk=None):
        source_account = self.get_object()
        serializer = BuyGoodsSerializer(data=request.data, context={'account': source_account})
        serializer.is_valid(raise_exception=True)
        try:
            transaction = serializer.save()
        except ValidationError as e:
            return handle_validation_error(e)
        return self.success_response(request, transaction,message='Payment successful')
    
    @action(detail=True, methods=['post'])
    def pay_bill(self, request, pk=None):
        source_account = self.get_object()
        serializer = PayBillSerializer(data=request.data, context={'account': source_account})
        serializer.is_valid(raise_exception=True)
        try:
            transaction = serializer.save()
        except ValidationError as e:
            return handle_validation_error(e)
        return self.success_response(request, transaction,message='Payment successful')
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        account = self.get_object()
        transactions = account.mini_statement()
        serializer = TransactionSerializer(transactions, many=True,context={'request': request})
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'])
    def statement(self, request, pk=None):
        account = self.get_object()

        # Parse query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        num_transactions_str = request.query_params.get('num_transactions')

        # Set default values
        num_transactions = int(num_transactions_str) if num_transactions_str else 100
        end_date = datetime.now().date()
        start_date = end_date.replace(day=1)

        # Parse date strings
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Generate statement
        transactions = account.generate_statement(num_transactions, start_date, end_date)
        serializer = TransactionSerializer(transactions, many=True,context={'request': request})
        return Response(serializer.data)
    
    
    def success_response(self, request, transaction,message):
        return Response({'status': message, 'transaction': TransactionSerializer(transaction,context={'request':request}).data})



    class CardViewSet(viewsets.ModelViewSet):
        serializer_class = CardSerializer
        
        def get_queryset(self):
            account_pk = self.kwargs['account_pk']
            return Card.objects.filter(account__pk=account_pk)

        def get_object(self):
            queryset = self.get_queryset()
            card_pk = self.kwargs['pk']
            obj = get_object_or_404(queryset, pk=card_pk)
            return obj
        
        def list(self, request,account_pk=None, pk=None):
            queryset = self.get_queryset()
            serializer = CardSerializer(queryset, many=True,context={'request': request})
            return Response(serializer.data)
        
        
        def create(self, request,account_pk=None, pk=None):
            account = get_object_or_404(Account, pk=account_pk)
            serializer = CardSerializer(data=request.data,context={'account':account})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        @action(detail=True, methods=['post'],url_path='card_deposit')
        def card_deposit(self, request, account_pk=None, pk=None):
            card = self.get_object()
            serializer = CardDepositSerializer(data=request.data,context={'card': card})
            serializer.is_valid(raise_exception=True)
            try:
                transaction = serializer.save()
            except ValidationError as e:
                return handle_validation_error(e)
            return self.success_response(request, transaction,message='Funds Deposit to Gift Card successful')


        @action(detail=True, methods=['post'], url_path='card_redeem')
        def card_redeem(self, request, account_pk=None, pk=None):
            card = self.get_object()
            serializer = CardRedeemSerializer(data=request.data,context={'card': card})
            serializer.is_valid(raise_exception=True)
            try:
                transaction = serializer.save()
            except ValidationError as e:
                return handle_validation_error(e)
            return self.success_response(request, transaction,message='Funds Redeem from Gift Card successful')



        @action(detail=True, methods=['post'], url_path='card_refund')
        def card_refund(self, request, account_pk=None, pk=None):
            card = self.get_object()
            serializer = CardRefundSerializer(data=request.data,context={'card': card})
            serializer.is_valid(raise_exception=True)
            try:
                transaction = serializer.save()
            except ValidationError as e:
                return handle_validation_error(e)
            return self.success_response(request, transaction,message='Funds Redeem from Gift Card successful')

        @action(methods=['post'], detail=True,url_path='card_transfer')
        def card_transfer(self, request,account_pk=None, pk=None):
            card = self.get_object()
            serializer = CardTransferSerializer(data=request.data, context={'card': card})
            serializer.is_valid(raise_exception=True)
            try:
                transaction = serializer.save()
            except ValidationError as e:
                return handle_validation_error(e)
            return self.success_response(request, transaction,message='Funds Redeem from Gift Card successful')

        
        @action(detail=True, methods=['post'], url_path='card_deactivate')
        def deactivate(self, request,account_pk=None, pk=None):
            card = self.get_object()
            serializer = DeactivateCardSerializer(data=request.data,context={'card':card,'request':request})
            serializer.is_valid(raise_exception=True)
            try:
                transaction = serializer.save()
            except ValidationError as e:
                return handle_validation_error(e)
            return Response({'status':'Gift Card Deactivation successful'})

        
        def success_response(self, request, transaction,message):
            return Response({'status': message, 'transaction': TransactionSerializer(transaction,context={'request':request}).data})

    
