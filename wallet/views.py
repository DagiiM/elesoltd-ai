from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def wallet_index(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/index.html',context)

@login_required
def tp2c_funds_transfer(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/tp2c_funds_transfer.html',context)

@login_required
def c2c_internal_funds_transfer(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/c2c_internal_funds_transfer.html',context)

@login_required
def c2tp_funds_transfer(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/c2tp_funds_transfer.html',context)

@login_required
def c2c_buy_goods_and_services(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/c2c_buy_goods_and_services.html',context)

@login_required
def c2b_funds_debit(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/c2b_funds_debit.html',context)

@login_required
def b2c_funds_credit(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/b2c_funds_credit.html',context)

@login_required
def transaction_short_statement(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/transaction_short_statement.html',context)

@login_required
def transaction_full_statement(request,account=1):
    context = {'account': account,'app_name': settings.APP_NAME}
    return render(request, 'wallet/transaction_full_statement.html',context)

