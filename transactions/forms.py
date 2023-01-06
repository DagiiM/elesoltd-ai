from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class TransferForm(forms.Form):
    recipient = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date = forms.DateField()

class SchedulePaymentForm(forms.Form):
    recipient = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date = forms.DateField()

class CancelScheduledPaymentForm(forms.Form):
    payment_id = forms.IntegerField()
