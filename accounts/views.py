from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic import ListView, DetailView
from .forms import AccountForm, StatementForm, TransactionForm, ScheduledPaymentForm, TransferForm,AccountUpdateForm
from .models import Account

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
        context['form'] = TransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            date = form.cleaned_data['date']
            self.object.add_transaction(amount, transaction_type, date)
            return redirect('accounts:account_detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)



def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            messages.success(request, 'Account created successfully')
            return redirect(request, 'accounts:account_list')
        else:
            messages.error(request, 'Error creating account')
    else:
        form = AccountForm()
    return render(request, 'accounts/create_account.html', {'form': form})


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


def account_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Account, pk=pk).delete()
        messages.success(request, 'Account deleted successfully')
    return redirect(request, 'accounts:account_list')

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

def add_scheduled_payment(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = ScheduledPaymentForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            frequency = form.cleaned_data['frequency']
            payment_id = account.add_scheduled_payment(recipient, amount, frequency)
            messages.success(request, f'Scheduled payment added with ID: {payment_id}')
            return redirect(reverse('accounts:account_detail', kwargs={'pk': pk}))
    else:
        form = ScheduledPaymentForm()
    return render(request, 'accounts/add_scheduled_payment.html', {'form': form})

def scheduled_payments(request, pk):
    account = get_object_or_404(Account, pk=pk)
    scheduled_payments = account.scheduled_payments()
    return render(request, 'accounts/scheduled_payments.html', {'scheduled_payments': scheduled_payments})

def transfer(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            account.transfer(recipient, amount)
            messages.success(request, 'Transfer successful')
            return redirect(reverse('accounts:account_detail', kwargs={'pk': pk}))
    else:
        form = TransferForm()
    return render(request, 'accounts/transfer.html', {'form': form})

