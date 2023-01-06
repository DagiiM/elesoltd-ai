from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=255)
    shipping_street = forms.CharField(max_length=255)
    shipping_city = forms.CharField(max_length=255)
    shipping_state = forms.CharField(max_length=255)
    shipping_zip_code = forms.CharField(max_length=255)
    billing_street = forms.CharField(max_length=255)
    billing_city = forms.CharField(max_length=255)
    billing_state = forms.CharField(max_length=255)
    billing_zip_code = forms.CharField(max_length=255)
    payment_method = forms.CharField(max_length=255)
