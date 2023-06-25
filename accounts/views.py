from django.shortcuts     import render, redirect
from django.views.generic import View
from django.contrib       import messages

from random import randint

from .forms  import UserPhoneNumberRegistrationForm, OtpVerificationForm

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register/register.html")

class PhoneNumberRegisterView(View):
    form_class = UserPhoneNumberRegistrationForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register/phone_number.html', {"form": form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "کد فعال سازی حساب ارسال شد")
            return redirect('accounts:otp-verification')
        else:
            return render(request, 'accounts/register/phone_number.html', {"form": form}, status=400)


class OtpCodeVerificationView(View):
    form_class = OtpVerificationForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register/verify_phone.html', {"form": form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.create()
        else:
            return render(request, 'accounts/register/verify_phone.html', {"form": form}, status=400)
        return redirect('accounts:register')