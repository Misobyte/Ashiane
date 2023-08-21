import pyotp
import base64
import os

from django.core.mail import send_mail

from .models import OtpCode


def generate_otp_code():
    totp = pyotp.TOTP(base64.b32encode(os.urandom(16)).decode('utf-8'))
    otp = totp.now()
    return otp

def send_otp_code(instance):
    otp = generate_otp_code()
    otp_object = OtpCode.objects.create(otp_code=otp)
    instance.otp_code = otp_object
    if instance.auth_method == "email":
        send_mail(
            "کد تایید شما برای وبسایت آشیانه",
            f"کد تایید: {otp}",
            "Ashiane",
            [instance.email],
            fail_silently=False,
        )
    elif instance.auth_method == "number":
        print(instance.phone_number, otp)
    return instance