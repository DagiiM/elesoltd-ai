from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .forms import AccountForm, StatementForm, AccountUpdateForm, DepositForm, WithdrawForm, TransferForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse

class AccountListView(ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'accounts/account_list.html'
    paginate_by = 10


class AccountDetailView(DetailView):
    model = Account
    context_object_name = 'account'
    template_name = 'accounts/account_detail.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.get_object()
        context['transactions'] = account.generate_statement()
        return context

@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        # Check if the user is authenticated and is the owner of the account
        if request.user.is_authenticated and request.user == account.user:
            form = AccountUpdateForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return redirect('account_detail', pk=account.pk)
    else:
        # Check if the user is authenticated and is the owner of the account
        if request.user.is_authenticated and request.user == account.user:
            form = AccountUpdateForm(instance=account)
            return render(request, 'accounts/account_update.html', {'form': form})
    # If the user is not authenticated or is not the owner of the account, redirect them
    return redirect('login')

@login_required
def generate_statement(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = StatementForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            statement = account.generate_statement(start_date, end_date)
            return render(request, 'accounts/statement.html', {'statement': statement})
    else:
        form = StatementForm()
    return render(request, 'accounts/generate_statement.html', {'form': form})


@login_required
def deposit(request):
    if request.method == 'POST':
        print('Good')
        form = DepositForm(request.POST)
        if form.is_valid():
            customer = request.user
            customer_account = customer.account_set.get()
            transaction_type = 'deposit' 
            payment_method = 'mpesa'
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            
            transaction = Transaction.objects.create(
                customer=customer,
                beneficiary=customer,
                account=customer_account,
                transaction_type=transaction_type,
                payment_method=payment_method,
                amount=amount,
                description=description
            )
            context = {
                'reference_number': transaction.reference_number,
                'customer': {
                    'first_name': transaction.customer.first_name,
                    'last_name': transaction.customer.first_name,
                },
                'beneficiary': {
                    'first_name': transaction.customer.first_name,
                    'last_name': transaction.customer.first_name,
                },
                'amount': transaction.amount,
                'description': transaction.description
            }
            
            return JsonResponse(context)
    else:
        form = DepositForm()
    return render(request, 'accounts/deposit.html', {'form': form})

def withdraw(request):
    customer = request.user
    account = customer.account_set.get()
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            
           return redirect('account_detail', pk=account.pk)
    else:
        form = WithdrawForm()
    return render(request, 'accounts/withdraw.html', {'form': form})

def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            customer = request.user
            transaction_type = 'transfer' 
            payment_method = 'internal'
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            beneficiary_acccount = Account.objects.get(account_number=form.cleaned_data['beneficiary'])
            
            transaction = Transaction.objects.create(
                customer=customer,
                beneficiary=beneficiary_acccount.user,
                account=beneficiary_acccount,
                transaction_type=transaction_type,
                payment_method=payment_method,
                amount=amount,
                description=description
            )
            context = {
                'transaction': transaction.reference_number,
                'customer': {
                    'first_name': transaction.customer.first_name,
                    'last_name': transaction.customer.first_name,
                },
                'beneficiary': {
                    'first_name': transaction.customer.first_name,
                    'last_name': transaction.customer.first_name,
                },
                'payment_method': payment_method,
                'amount': transaction.amount,
                'description': transaction.description
            }
            
            return JsonResponse(context)
    else:
        form = TransferForm()
    return render(request, 'accounts/transfer.html', {'form': form})