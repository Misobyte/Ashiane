from django                       import forms
from django.core.exceptions       import ValidationError
from django.utils.translation     import gettext_lazy as _
from django.contrib               import messages
from django.contrib.auth          import get_user_model, password_validation
from django.contrib.auth.forms    import UserChangeForm as BaseUserChangeForm, BaseUserCreationForm, UsernameField
from django.db.models             import Q

from phonenumber_field.formfields import PhoneNumberField

from .models import OtpCode, User
from .utils  import generate_otp_code, send_otp_code, send_otp_code_email

User = get_user_model()

class AdminUserCreationForm(BaseUserCreationForm):
    phone_number = PhoneNumberField(label="شماره تلفن")

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password_repeat = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("username", "phone_number", "password")
        field_classes = {"username": UsernameField}

class AdminUserChangeForm(BaseUserChangeForm):
    pass

class UserRegistrationFormBase(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password_repeat = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = User
        fields = "__all__"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password_repeat")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)


class UserPhoneNumberRegistrationForm(UserRegistrationFormBase):
    phone_number = PhoneNumberField(label="شماره تلفن")

    class Meta:
        model = User
        fields = ["username", "phone_number", "password"]
        field_classes = {"username": UsernameField}
    
    def save(self, commit):
        instance = super(UserPhoneNumberRegistrationForm, self).save(commit=False)
        otp = generate_otp_code()
        otp_object = OtpCode.objects.create(otp_code=otp)
        instance.otp_code = otp_object
        instance.password = self.cleaned_data.get("password")
        instance.auth_method = "number"
        if commit:
            instance.save()
            send_otp_code(self.cleaned_data.get("phone_number"), otp)
        return instance



class UserEmailRegistrationForm(UserRegistrationFormBase):
    email = forms.EmailField(label=_("ایمیل"))

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        field_classes = {"username": UsernameField}
    
    def save(self, commit):
        instance = super(UserEmailRegistrationForm, self).save(commit=False)
        otp = generate_otp_code()
        otp_object = OtpCode.objects.create(otp_code=otp)
        instance.otp_code = otp_object
        instance.password = self.cleaned_data.get("password")
        instance.auth_method = "email"
        if commit:
            instance.save()
            send_otp_code_email(self.cleaned_data.get("email"), otp)
        return instance


class OtpVerificationForm(forms.Form):
    otp = forms.CharField(required=True, label="کد فعال سازی")

    def _post_clean(self):
        super()._post_clean()
        if not self.user.otp_code.otp_code == self.cleaned_data.get("otp"):
            self.add_error("otp", "کد فعال سازی اشتباه وارد شده")
        elif not self.user.otp_code.is_valid():
            self.add_error("otp", "کد فعال سازی منقضی شده. دوباره ارسال شد")
            otp = generate_otp_code()
            self.user.otp_code.otp_code = otp
    
    def create(self):
        self.user.is_active = True
        if self.user.auth_method == "email":
            self.user.email_verfied = True
        elif self.user.auth_method == "number":
            self.user.phone_number_verified = True
        self.user.save()
    
    def __init__(self, username, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = User.objects.filter(username=username).first()