from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountListView.as_view(), name='account_list'),
    path('<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('<int:pk>/update/', views.account_update, name='account_update'),
    path('<int:pk>/statement/', views.generate_statement, name='generate_statement'),
    path('deposit', views.deposit, name='deposit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('transfer', views.transfer, name='transfer'),
]