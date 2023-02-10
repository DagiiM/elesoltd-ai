from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
import os

from django.db import models

class OrderItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

class Order(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiration_date = models.CharField(max_length=255)
    cvv = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.CharField(max_length=255,default=False)
    # Use a ForeignKey field to link to a separate model for items
   # items = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    # Use a ForeignKey field to link to a separate model for shipping address
   # shipping_address = models.ForeignKey(Address, related_name="shipping_address", on_delete=models.CASCADE)
    # Use a ForeignKey field to link to a separate model for billing address
   # billing_address = models.ForeignKey(Address, related_name="billing_address", on_delete=models.CASCADE)
   # payment_method = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneNumber = models.CharField(null=True, blank=True,max_length=100)
    phoneId = models.CharField(null=True, blank=True,max_length=200)
    #Utility Variables
    uniqueId = models.CharField(null=True, blank=True,unique=True,max_length=100)
    date_created = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    
    def save(self,*args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime[timezone.now()]
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.locatime(timezone.now())
        super(Profile, self).save(*args, **kwargs)
       
         
class BusinessPlan(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company_description = models.TextField(null=True, blank=True)
    market_analysis = models.TextField(null=True, blank=True)
    swot_analysis = models.TextField(null=True, blank=True)
    product_detail = models.TextField(null=True, blank=True)
    marketing_strategy = models.TextField(null=True, blank=True)
    def save(self,*args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime[timezone.now()]
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.locatime(timezone.now())
        super(BusinessPlan, self).save(*args, **kwargs)


      
# Create your models here.

class ChatSession(models.Model):
    OPTIONS = [
        ['(Pty) Ltd','(Pty) Ltd'],
        ['Non-Profit','Non-Profit'],
        ['Partnership','Partnership'],
    ]
    
    email_address = models.EmailField(blank=True, null=True)
    business_name = models.TextField(null=True,blank=True)
    business_type = models.TextField(null=True,blank=True)
    country = models.TextField(null=True,blank=True)
    product_service = models.TextField(null=True,blank=True)
    short_description = models.TextField(null=True,blank=True)
    years = models.IntegerField(null=True,blank=True)
    progress = models.TextField(null=True,blank=True)
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    uniqueId = models.CharField(null=True,blank=True,unique=True,max_length=100)
    date_created = models.DateTimeField(null=True,blank=True)
    last_updated = models.DateTimeField(null=True,blank=True)
    
    def save(self,*args, **kwargs):
        if self.date_created is None:
            self.date_created=timezone.localtime[timezone.now()]
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
        self.last_updated = timezone.locatime(timezone.now())
        super(ChatSession, self).save(*args, **kwargs)
         
        
        
        
        
    ## class FinancialModel():