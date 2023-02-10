from django.db import models
from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
 
class LoginForm(forms.Form):
    #email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    