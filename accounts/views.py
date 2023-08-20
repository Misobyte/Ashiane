from django.shortcuts     import render, redirect
from django.views.generic import View
from django.contrib       import messages

from random import randint

from .forms  import UserPhoneNumberRegistrationForm, UserEmailRegistrationForm, OtpVerificationForm
from .models import User

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register/register.html")

class PhoneNumberRegisterView(View):
    form_class = UserPhoneNumberRegistrationForm
    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register/phone_number.html", {"form": form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)
            request.session["username"] = instance.username
            messages.success(request, "کد فعال سازی حساب ارسال شد")
            return redirect("accounts:otp-verification")
        else:
            return render(request, "accounts/register/phone_number.html", {"form": form}, status=400)


class EmailRegisterView(View):
    form_class = UserEmailRegistrationForm
    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/register/email.html", {"form": form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)
            request.session["username"] = instance.username
            messages.success(request, "کد فعال سازی حساب ارسال شد")
            return redirect("accounts:otp-verification")
        else:
            return render(request, "accounts/register/email.html", {"form": form}, status=400)


class OtpCodeVerificationView(View):
    form_class = OtpVerificationForm

    def setup(self, request, *args, **kwargs):
        self.username = request.session.get("username", None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.username:
            messages.error(request, "شما برای دسترسی به این صفحه نیاز به ثبت نام دارید")
            return redirect("accounts:register")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request=request, username=self.username)
        return render(request, "accounts/register/verify_phone.html", {"form": form})
    
    def post(self, request):
        form = self.form_class(request=request, username=self.username, data=request.POST)
        if form.is_valid():
            form.create()
            del request.session["username"]
        else:
            return render(request, "accounts/register/verify_phone.html", {"form": form}, status=400)
        return redirect("accounts:register")