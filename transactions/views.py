from django.shortcuts import render, redirect, get_object_or_404
from .forms import DepositForm, WithdrawForm, TransferForm, PaymentForm, SchedulePaymentForm, CancelScheduledPaymentForm
from accounts.models import Account
from django.http import HttpResponse
from .models import Transaction
from .apis.payment import PayPalAPI, MpesaAPI, PrepaidCardAPI

def deposit(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account.deposit(form.cleaned_data['amount'])
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = DepositForm()
    return render(request, 'transactions/deposit.html', {'form': form})

def withdraw(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            account.withdraw(form.cleaned_data['amount'])
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = WithdrawForm()
    return render(request, 'transactions/withdraw.html', {'form': form})

def transfer(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            account.transfer(recipient, amount)
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = TransferForm()
    return render(request, 'transactions/transfer.html', {'form': form})

def payment(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            account.add_transaction(form.cleaned_data['amount'], 'PAYMENT', form.cleaned_data['date'])
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = PaymentForm()
    return render(request, 'transactions/payment.html', {'form': form})

def schedule_payment(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = SchedulePaymentForm(request.POST)
        if form.is_valid():
            account.schedule_payment(form.cleaned_data['recipient'], form.cleaned_data['amount'], form.cleaned_data['date'])
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = SchedulePaymentForm()
    return render(request, 'transactions/schedule_payment.html', {'form': form})

def cancel_scheduled_payment(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = CancelScheduledPaymentForm(request.POST)
        if form.is_valid():
            account.cancel_scheduled_payment(form.cleaned_data['payment_id'])
            account.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = CancelScheduledPaymentForm()
    return render(request, 'transactions/cancel_scheduled_payment.html', {'form': form})

  # Third party payments

def make_payment(request):
    if request.method == "POST":
        api_name = request.POST["api"]
        if api_name == "paypal":
            api = PayPalAPI()
        elif api_name == "mpesa":
            api = MpesaAPI()
        elif api_name == "prepaid_card":
            api = PrepaidCardAPI()
        else:
            return HttpResponse(status=400)
        
        amount = request.POST["amount"]
        try:
            tax_rate = request.POST["tax_rate"]
        except KeyError:
            tax_rate = 0
        try:
            discount_rate = request.POST["discount_rate"]
        except KeyError:
            discount_rate = 0
        
        total_amount = api.calculate_tax(amount, tax_rate) + amount
        final_amount = api.apply_discount(total_amount, discount_rate)
        charge_response = api.charge(final_amount)
        charge_id = charge_response["id"]
        
        payment = Transaction.objects.create(
            api=api_name,
            charge_id=charge_id,
            amount=final_amount,
            discount_rate=discount_rate,
            tax_rate=tax_rate,
        )
        
        return render(request, "payment_success.html", {"payment": payment})
    else:
        return render(request, "make_payment.html")

def refund_payment(request, payment_id):
    payment = get_object_or_404(Transaction, pk=payment_id)
    if payment.api == "paypal":
        api = PayPalAPI()
    elif payment.api == "mpesa":
        api = MpesaAPI()
    elif payment.api == "prepaid_card":
       api = PrepaidCardAPI()
    else:
        return HttpResponse(status=400)

    refund_response = api.refund(payment.charge_id)
    payment.refunded = True
    payment.save()

    return render(request, "refund_success.html", {"payment": payment})

def paypal_auth(request):
    paypal = PayPalAPI(client_id="your_client_id", client_secret="your_client_secret", redirect_uri="http://localhost:8000/payments/paypal/auth")
    return paypal.authenticate(request)