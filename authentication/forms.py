from django import forms
from .models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
 
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    
class UserChangeForm(BaseUserChangeForm):
    password = forms.CharField(label='Password', widget=forms.HiddenInput)

    class Meta(BaseUserChangeForm.Meta):
        model = User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # check if user exists with the given login value
        user = None
        try:
            # try to get user by username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                # try to get user by email
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                try:
                    # try to get user by phone_number
                    user = User.objects.get(phone_number=username)
                except User.DoesNotExist:
                    pass

        # authenticate user
        if user:
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            elif not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
        else:
            raise forms.ValidationError("User does not exist with the given login value.")

        # return cleaned data along with username
        cleaned_data['username'] = user.username
        return cleaned_data
        