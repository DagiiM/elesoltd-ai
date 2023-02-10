from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'balance']
        #fields = '__all__'
        widgets = {
            'user': forms.HiddenInput()
        }
        
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'account_number', 'balance', 'currency',
                  'creation_date', 'status']


class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=200)
        
class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class TransferForm(forms.Form):
    beneficiary = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=200)

class StatementForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    
