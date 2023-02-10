from django.shortcuts import render
from django.conf import settings

# Create your views here.
def hire_request(request):
    
    return render(request, 'contact/contact.html');

def support_request(request):
    
    return render(request, 'contact/support.html');

def about(request):
    
    return render(request, 'contact/about.html');

def privacy_policy(request):
    context = {
        'support_email':settings.EMAIL_SUPPORT
    }
    return render(request, 'contact/privacy-policy.html',context);

def terms_and_conditions(request):
    context = {
        'company_name':settings.APP_NAME,
        'support_email':settings.EMAIL_SUPPORT
    }
    return render(request, 'contact/terms-conditions.html',context);
