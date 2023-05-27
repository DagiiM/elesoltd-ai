from django.db import models
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sessions.models import Session
from authentication.models import User

def send_email_notification(subject, message, to_email):
    try:
        send_mail(subject, message, "douglasmutethia@gmail.com", [to_email])
    except BadHeaderError:
        return 'Invalid header found.'
    except Exception as e:
        return str(e)
    
def send_sms_notification(message, to):
    return 'success'
   # pass  # Implement SMS sending logic here

def save_to_database(subject, message, to):
    pass
    
class DeliveryMethod(models.TextChoices):
    EMAIL = 'email'
    SMS = 'sms'
    DATABASE = 'database'

class Notification(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethod.choices,
        default=DeliveryMethod.EMAIL
    )
    status = models.CharField(max_length=20, default='pending')
    to = models.TextField()
    #user = models.ForeignKey(User,on_delete=models.CASCADE)

    def send_notification(self):
        to_list = self.to.split(',')
        for recipient in to_list:
            if self.delivery_method == DeliveryMethod.EMAIL:
                result = send_email_notification(self.subject, self.message, recipient)
                if result is None:
                    self.status = 'delivered'
                else:
                    self.status = 'failed'
            elif self.delivery_method == DeliveryMethod.SMS:
                result = send_sms_notification(self.message, recipient)
                if result is None:
                    self.status = 'delivered'
                else:
                    self.status = 'failed'
            elif self.delivery_method == DeliveryMethod.DATABASE:
                result = save_to_database(self.subject, self.message, recipient)
                if result is None:
                    self.status = 'delivered'
                else:
                    self.status = 'failed'
        self.save()
