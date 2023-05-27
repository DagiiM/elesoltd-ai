from django import forms
from .models import Account
from authentication.models import User     
from django import forms
from django.core.validators import RegexValidator
from .models import Account

class AccountForm(forms.ModelForm):
    '''
    account_number = forms.CharField(
        validators=[RegexValidator(r'^\d+$', 'Account number must be a number')],
    )
    '''
    balance = forms.DecimalField(disabled=True)
    max_balance = forms.DecimalField(disabled=True)
    #user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select)

    class Meta:
        model = Account
        fields = ['account_type', 'status', 'currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].initial = 0.00
        self.fields['max_balance'].initial = 9999999.00
        self.fields['user'].label = 'User'
        
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'balance', 'currency',
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
    
