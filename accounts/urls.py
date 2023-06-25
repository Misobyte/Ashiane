from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/phone_number/", views.PhoneNumberRegisterView.as_view(), name="phone-number-register"),
    path("register/phone_number/verify/", views.OtpCodeVerificationView.as_view(), name="otp-verification"),
]
