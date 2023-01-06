from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'balance']
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput()
        }
        
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'account_number', 'balance', 'currency', 'transaction_history',
                  'creation_date', 'status', 'address', 'phone_number', 'language', 'time_zone',
                  'billing_address', 'payment_methods', 'referral_code', 'occupation', 'income',
                  'credit_score']


class TransactionForm(forms.Form):
    amount = forms.DecimalField()
    transaction_type = forms.ChoiceField(choices=[('debit', 'Debit'), ('credit', 'Credit')])

class ScheduledPaymentForm(forms.Form):
    amount = forms.DecimalField()
    recipient = forms.CharField()
    date = forms.DateField()
    frequency = forms.ChoiceField(choices=[('once', 'Once'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])

class TransferForm(forms.Form):
    amount = forms.DecimalField()
    recipient = forms.CharField()

class StatementForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    
