from django.shortcuts import render

# Create your views here.
def display_notification(request):
    return render(request, 'notifications/notification.html')