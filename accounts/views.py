from django.contrib            import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions    import ValidationError
from django.shortcuts          import render, redirect
from django.views.generic      import View
from django.shortcuts          import redirect

from random import randint

from .forms  import UserPhoneNumberRegistrationForm, UserEmailRegistrationForm, OtpVerificationForm
from .models import User
from .utils import send_otp_code

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


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_activated:
            user = send_otp_code(user)
            user.save()
            self.request.session["username"] = user.username
            return redirect("accounts:otp-verification")
        else:
            return super().form_valid(form)