
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from rest_framework.decorators import action
# New Code
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import User
from django.core.mail import send_mail
from django.urls import reverse
from .serializers import (UserSerializer,
                          PasswordResetSerializer,
                          ChangePasswordSerializer,
                          LoginSerializer,
                          PasswordResetConfirmSerializer)
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    actions = {
        'create': ['post'],
        'update': ['put', 'patch'],
        'destroy': ['delete'],
        #'retrieve': ['get'],
        'password_reset': ['post'],
        'change_password': ['post'],
        'login': ['post'],
    }

    def get_serializer_class(self):
        if self.action == 'password_reset':
            return PasswordResetSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        elif self.action == 'login':
            return LoginSerializer
        else:
            return super().get_serializer_class()

    @action(detail=False,methods=['post','get'])
    def password_reset(self, request,pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if user:
            token = serializer.save(user)
            reset_url = request.build_absolute_uri(reverse('resetpassword_validate', kwargs={'uidb64': token[0], 'token': token[1]}))
            send_mail(
                'Password reset',
                f'Use the following link to reset your password: {reset_url}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )
        return Response({'message': 'Password reset instructions have been sent to your email address.'}, status=status.HTTP_200_OK)
    
    
    @action(methods=['post'], detail=True,url_path='change-password', url_name='change_password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'message': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=False,methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

       
       
def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError,User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
         request.session['uid'] = uid
         data = {
             "message":"Please reset your password",
         }
         #messages.success(request,"Please reset your password")
         return redirect('resetPassword')
    else:
         #messages.error(request,"Activation link is invalid or has expired.")
         data = {
             "message":"Activation link is invalid or has expired.",
         }
         
        
from rest_framework.decorators import api_view
@api_view(['GET','POST'])
def resetPassword(request):
    if request.method == 'GET':
        return render(request, 'password_reset_confirm.html')
    elif request.method == 'POST':
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = request.session['uid']
            user = User.objects.get(pk=uid)
            serializer.save(user=user)
            return Response({"success": True})
        else:
            return Response(serializer.errors)


def password_reset_done(request):
    return render(request, 'auth/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'auth/password_reset_complete.html')

from django.contrib.auth import logout

@login_required(login_url='/login')
def view_logout(request):
    logout(request)
    return render(request, 'login.html')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'auth/dashboard.html')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError,User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()      
        messages.success(request,'Congratulations! Your Account is activated.')
        return redirect('login')
    else:
        messages.error(request,'Activation link is invalid or has expired.')
        return redirect('register')
    
def register(request):
    return render(request, 'register.html')

def view_login(request):
    return render(request, 'login.html')

def view_forgot_password(request):
    return render(request, 'forgot_password.html')