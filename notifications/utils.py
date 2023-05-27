from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from decouple import config

def mail_notification(recipient,
                      subject, 
                      message, 
                      attachment_path=None,
                      attachment="file.pdf"
                      ):
    # Set up the email message
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=config('EMAIL_HOST_USER'),
        to=[recipient],
    )

    # Attach the file if an attachment path is provided
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            email.attach(attachment, f.read(), 'application/pdf')

    # Send the email
    email.send()



def send_activation_email(user, email):
    current_site = config('APP_NAME')
    mail_subject = 'Please Activate your account.'
    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': config('APP_DOMAIN'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()

