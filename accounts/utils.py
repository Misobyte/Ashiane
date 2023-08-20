from django.core.mail import send_mail
import pyotp
import base64
import os


def generate_otp_code():
    totp = pyotp.TOTP(base64.b32encode(os.urandom(16)).decode('utf-8'))
    otp = totp.now()
    return otp

def send_otp_code(pn, code):
    print(pn, code)

def send_otp_code_email(email, code):
    send_mail(
        "کد تایید شما برای وبسایت آشیانه",
        f"کد تایید: {code}",
        "Ashiane",
        [email],
        fail_silently=False,
    )
    print("sent to " + email)
    print(email, code)