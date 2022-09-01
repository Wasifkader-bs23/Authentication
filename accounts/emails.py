from pyexpat.errors import messages
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User

def send_otp_via_email(email):
    subject=f'Your account verification email'
    otp=random.randint(1000,  9999)
    print(otp)
    message=f'your otp is {otp}'
    print(message)
    email_from=settings.EMAIL_HOST
    send_mail(subject, message,email_from,[email])
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()