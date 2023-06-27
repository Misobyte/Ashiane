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
        return render(request, "accounts/register/phone_number.html", {"form": form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=True)
            request.session["otp-verify-id"] = instance.username
            messages.success(request, "کد فعال سازی حساب ارسال شد")
            return redirect("accounts:otp-verification")
        else:
            return render(request, "accounts/register/phone_number.html", {"form": form}, status=400)


class OtpCodeVerificationView(View):
    form_class = OtpVerificationForm
    def get(self, request):
        print(request.session.get("otp-verify-id"))
        form = self.form_class(pending_username=request.session.get("otp-verify-id", None))
        
        return render(request, "accounts/register/verify_phone.html", {"form": form})
    def post(self, request):
        form = self.form_class(pending_username=request.session.get("otp-verify-id", None), data=request.POST)
        if form.is_valid():
            form.create()
        else:
            if "کد فعال سازی منقضی شده است . لطفا مجددا ثبت نام نمایید" in form.errors["otp"]:
                del request.session["otp-verify-id"]
            return render(request, "accounts/register/verify_phone.html", {"form": form}, status=400)
        return redirect("accounts:register")