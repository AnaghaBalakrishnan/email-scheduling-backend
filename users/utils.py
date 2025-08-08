# users/utils.py
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import User

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_email(email):
    otp = generate_otp()
    try:
        user = User.objects.get(email=email)
        user.otp = otp
        user.otp_expiry = timezone.now() + timedelta(minutes=5) # OTP expires in 5 minutes [cite: 27]
        user.save()

        # Send OTP email [cite: 25]
        subject = 'Your Account Verification OTP'
        message = f'Your OTP to verify your account is: {otp}'
        from_email = 'no-reply@yourapp.com' # Use your configured email
        send_mail(subject, message, from_email, [email])

    except User.DoesNotExist:
        # Handle case where user does not exist, though this shouldn't happen in the registration flow
        return None