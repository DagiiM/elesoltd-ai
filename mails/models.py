from django.db import models

class Email(models.Model):
    subject = models.CharField(max_length=200)
    sender = models.EmailField()
    recipient = models.EmailField()
    cc = models.EmailField(blank=True)
    bcc = models.EmailField(blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    send_time = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=50, blank=True)
    draft = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments', blank=True)
    
    def mark_as_read(self):
        self.read = True
        self.save()