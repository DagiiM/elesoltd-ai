from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    api = models.CharField(default='internal',max_length=20)
    charge_id = models.CharField(max_length=100)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    refunded = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
