from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountListView.as_view(), name='account_list'),
    path('create/', views.create_account, name='create_account'),
    path('<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('<int:pk>/update/', views.account_update, name='account_update'),
    path('<int:pk>/delete/', views.account_delete, name='account_delete'),
    path('<int:pk>/statement/', views.generate_statement, name='generate_statement'),
    path('<int:pk>/scheduled-payments/', views.scheduled_payments, name='scheduled_payments'),
    path('<int:pk>/scheduled-payments/add/', views.add_scheduled_payment, name='add_scheduled_payment'),
    path('<int:pk>/transfer/', views.transfer, name='transfer'),
]