from django.urls import path
from . import views

urlpatterns = [
    path('wallet/',views.wallet_index,name="wallet"),
    path('wallet/deposit-to-my-account', views.tp2c_funds_transfer, name="tp2c_funds_transfer"),
    path('wallet/internal-funds-transfer', views.c2c_internal_funds_transfer, name="c2c_internal_funds_transfer"),
    path('wallet/external-funds-transfer', views.c2tp_funds_transfer, name="c2tp_funds_transfer"),
    path('wallet/buy-goods-and-services', views.c2c_buy_goods_and_services, name="c2c_buy_goods_and_services"),
    path('wallet/c2b-funds-debit', views.c2b_funds_debit, name="c2b_funds_debit"),
    path('wallet/b2c-funds-credit', views.b2c_funds_credit, name="b2c_funds_credit"),
    path('wallet/transaction-short-statement', views.transaction_short_statement, name="transaction_short_statement"),
    path('wallet/transaction-full-statement', views.transaction_full_statement, name="transaction_full_statement"),
]
