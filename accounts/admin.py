from django.contrib import admin
from .models import Transaction, Account,Card
from .models import Biller, Merchant
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

class BillerInline(admin.TabularInline):
    model = Biller
    extra=0
    fields = ['name', 'biller_number','email', 'address', 'phone']
    readonly_fields = ['biller_number']
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')
    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
class MerchantInline(admin.TabularInline):
    model = Merchant
    extra = 0
    list_display = ('name', 'till_number','email', 'address', 'phone')
    readonly_fields = ['till_number']
    show_change_link = True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    

@admin.register(Biller)
class BillerAdmin(admin.ModelAdmin):
    list_display = ('name','biller_number', 'account', 'email', 'phone', 'address',)
    list_filter = ('account',)
    search_fields = ('name', 'email', 'phone', 'address')
    raw_id_fields = ['account']

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name','till_number', 'account', 'email', 'phone', 'address')
    list_filter = ('account',)
    search_fields = ('name', 'email', 'phone', 'address')
    raw_id_fields = ['account']
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account','reference_number', 'transaction_type', 'amount', 'created_at')
    list_filter = ('transaction_type', 'payment_method', 'created_at')
    search_fields = ('reference_number', 'description')
    readonly_fields = ['account','payment_method','reference_number','transaction_type','amount','created_at','description',]
    ordering = ('-created_at',)
    def has_delete_permission(self, request, obj=None):
        # Prevent delete permission for all users
        return True
    def has_add_permission(self, request, obj=None):
        # Prevent add permission for all users
        return False
    def has_change_permission(self, request, obj=None):
        # Prevent edit permission for all users
        return False
    
class TransactionInline(admin.TabularInline):
    model = Transaction
    list_display = ('reference_number', 'transaction_type', 'amount', 'created_at')
    readonly_fields = list_display
    extra = 0
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # Define list_display using transaction fields
    list_display = ('reference_number', 'transaction_type', 'amount', 'created_at')
    # Define short descriptions for each field
    list_display_links = None
    list_display_links_details = None
    list_display_links_translations = None
    list_filter = None
    list_select_related = None
    list_per_page = 100

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')

class CardInline(admin.TabularInline):
    model = Card
    extra = 0
    show_change_link = True
    fieldsets = (
        (None, {
            'fields': ('masked_card_number','account', 'card_type', 'expiration_date', 'balance', 'is_active')
        }),
        (_('Limits'), {
            'fields': ('min_balance', 'max_balance'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('masked_card_number', 'cvv_code', 'expiration_date', 'min_balance', 'max_balance', 'created_at', 'updated_at')
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def save_model(self, request, obj, form, change):
        obj.harmonize_card_balance_with_account()
        super().save_model(request, obj, form, change)

    
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type', 'account_number', 'status', 'currency', 'balance']
    list_filter = ['account_type', 'status', 'currency', 'creation_date']
    search_fields = ['user__username', 'account_number']
    readonly_fields = ['user', 'account_number', 'currency', 'balance', 'max_balance', 'creation_date']
    raw_id_fields = ['user']
    actions = ['deactivate_accounts']
    inlines = [CardInline,BillerInline,MerchantInline,TransactionInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
    
    def deactivate_accounts(self, request, queryset):
        queryset.update(status='inactive')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.harmonize_card_balance_with_account()
        super().save_model(request, obj, form, change)
        
    list_display = ['id', 'account','masked_card_number','beneficiary','description', 'card_type','is_active']
    list_filter = ('card_type', 'is_active', 'created_at')
    search_fields = ('account__username', 'masked_card_number')
    readonly_fields = ('expiration_date','created_at', 'updated_at')
    raw_id_fields=['account']

    fieldsets = (
       # (None, {'fields': ('account','min_balance', 'max_balance',)}),
        ('Card details', {'fields': ('card_type',  'beneficiary','description','balance', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)})
    )

    def has_delete_permission(self, request, obj=None):
        return True
    
    def deactivate_accounts(self, request, queryset):
        queryset.update(status='inactive')
        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('account')

    