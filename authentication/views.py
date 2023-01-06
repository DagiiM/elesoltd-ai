from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from .forms import RegisterForm,LoginForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create a new user and redirect to the login page
           
            user = User.objects.create_user(
                        username = form.cleaned_data['username'],
                        email = form.cleaned_data['email'],
                        password = form.cleaned_data['password']
                    )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = form['email']
        password = form['password']
        user = authenticate(email='douglas@gmail.com', password='D12345678M')
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
           # messages.error(request, 'Invalid email or password')
            return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})




def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # send password reset email to the user's email address
            send_mail(
                'Password reset',
                'Please follow the link to reset your password: https://' + settings.APP_DOMAIN + '/reset/',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'auth/password_reset.html', {'form': form})

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # update the user's session token to prevent session hijacking
            update_session_auth_hash(request, form.user)
            # redirect to the home page
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/password_change.html', {'form': form})

def password_change_done(request):
    return render(request, 'auth/password_change_done.html')

def password_reset_confirm(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # update the user's session token to prevent session hijacking
                update_session_auth_hash(request, form.user)
                # redirect to the home page
                return redirect('home')
        else:
            form = SetPasswordForm(user)
        return render(request, 'auth/password_reset_confirm.html', {'form': form})
    else:
        # display an error message
        pass

def password_reset_done(request):
    return render(request, 'auth/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'auth/password_reset_complete.html')

def logout(request):
    logout(request)
    return redirect('login')