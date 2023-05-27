from django.urls import path
from notifications import views

urlpatterns = [
    path('notifications/', views.display_notification, name='notification'),
]
