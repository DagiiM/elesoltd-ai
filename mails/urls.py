from django.urls import path
from . import views

app_name = 'mails'

urlpatterns = [
    path('', views.email_list, name='email_list'),
    path('compose/', views.email_compose, name='email_compose'),
    path('<int:pk>/', views.email_detail, name='email_detail'),
    path('draft/<int:pk>/', views.email_draft, name='email_draft'),
    path('send/<int:pk>/', views.email_send, name='email_send'),
    path('delete/<int:pk>/', views.email_delete, name='email_delete'),
]
