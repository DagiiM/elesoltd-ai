from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
import os

from django.db import models
import openai

'''
import json       
import logging
import os
import urllib3
import requests_futures.sessions
from django.core.cache import cache
from django.core.management.base import BaseCommand
from cache_machine import CachedModel
from ratelimiter import RateLimiter

logger = logging.getLogger(__name__)

rate_limiter = RateLimiter(max_calls=100, period=60)  # Limit to 100 calls per minute

http = urllib3.PoolManager()

session = requests_futures.sessions.FuturesSession()

def get_completions(prompt, language=None, model="text-davinci-003"):
    cache_key = f"completions:{prompt}:{language}:{model}"
    completions = cache.get(cache_key)
    if completions is not None:
        return completions

    def on_success(resp):
        response = resp.json()
        completions = response['choices'][0]['text']
        cache.set(cache_key, completions, timeout=None)  # Cache indefinitely
        return completions

    def on_failure(exc):
        logger.error(f"Error making openai.completion API call: {exc}")
        return "Sorry, there was an error processing your request. Please try again later."

    api_key = os.environ.get(settings.OPENAI_API_KEY)
    params = {
        "prompt": prompt,
        "max_tokens": 2048,
        "stop": ".",
        "echo": False,
        "presence_penalty": 0,
        "best_of": 1,
        "stream": False,
        "stop_sequence": "",
        "temperature": 0.5,
        "top_p": 1,
    }
    if language:
        params["language"] = language
    if model:
        params["model"] = model
    url = f"https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    with rate_limiter:
        resp = session.post(url, json=params, headers=headers, background_callback=on_success, exception_callback=on_failure)
        return resp

class ChatCompletionQuerySet(models.QuerySet):
    def get_completions(self, prompt, language=None, model=None):
        cache_key = f"completions:{prompt}:{language}:{model}"
        completions = cache.get(cache_key)
        if completions is not None:
            return completions

        completions = get_completions(prompt, language=language, model=model)
        return completions

class ChatCompletionManager(models.Manager):
    def get_queryset(self):
        return ChatCompletionQuerySet(self.model, using=self._db)

    def create_completions(self, prompt, language=None, model=None):
        completions = self.get_queryset().get_completions(prompt, language=language, model=model)
        return self.create(prompt=prompt, completions=completions)


class ChatCompletion(CachedModel):
    prompt = models.TextField()
    completions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ChatCompletionManager()

    class Meta:
        cache_machine_cache_key_fields = ('prompt', 'language', 'model')
  
    def to_json(self):
        return {
            'id': self.pk,
            'prompt': self.prompt,
            'completions': self.completions,
            'created_at': self.created_at,
        }
    
    
    
    '''
'''import logging
import os
import requests
import urllib3
from django.core.management.base import BaseCommand
from django.core.cache import cache
import re
logger = logging.getLogger(__name__)

def sanitize_cache_key(key):
    return re.sub(r"[^\w\d_\-]", "", key)

session = requests.Session()
http = urllib3.PoolManager()
import openai

def get_completions(prompt, model=None):
    openai.api_key = settings.OPENAI_API_KEY

    # Set the model parameter
    if model:
        model = model
    else:
        model = "text-davinci-003"

    # Use the openai.Completion.create method to generate completions
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=2000,
        temperature=0,
        n=1,
        top_p=1,
        stop= "\n"
    )
    # Check the response status code
    if response.status != 200:
        logger.error(f"Failed to get completions: {response.text}")
        return []
    completions = response.json()["choices"][0]["text"]
    return completions

class ChatCompletionManager(models.Manager):
    def create_completions(self, prompt, model=None):
        completions = get_completions(prompt, model=model)
        return self.create(prompt=prompt, completions=completions)

class ChatCompletion(models.Model):
    prompt = models.TextField()
    completions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            "prompt": self.prompt,
            "completions": self.completions,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    objects = ChatCompletionManager()

class Command(BaseCommand):
    help = "Warm the cache for the openai.completion API completions"

    def handle(self, *args, **options):
        # Warm the cache with the most common completions
        common_prompts = [
            "Hello",
            "How are you?",
            "What is your name?",
            "Where are you from?",
            "What do you like to do?",
            "Tell me a joke.",
            "What is your favorite color?",
            "Do you have any pets?",
            "What is your favorite food?",
            "Do you have any hobbies?",
        ]
        for prompt in common_prompts:
            ChatCompletion.objects.create_completions(prompt, model="text-davinci-002")  # Provide the model parameter here

    
    '''

    
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
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    # Use a ForeignKey field to link to a separate model for items
    items = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    # Use a ForeignKey field to link to a separate model for shipping address
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", on_delete=models.CASCADE)
    # Use a ForeignKey field to link to a separate model for billing address
    billing_address = models.ForeignKey(Address, related_name="billing_address", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    
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