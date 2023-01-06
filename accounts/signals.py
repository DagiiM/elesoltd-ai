# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from .models import Account

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def ready(self):
    post_save.connect(create_user_account, sender=User)

