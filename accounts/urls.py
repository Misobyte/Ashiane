from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/phone_number/", views.PhoneNumberRegisterView.as_view(), name="phone-number-register"),
    path("register/email/", views.EmailRegisterView.as_view(), name="email-register"),
    path("register/verify/", views.OtpCodeVerificationView.as_view(), name="otp-verification"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
]
