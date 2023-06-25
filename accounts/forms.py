from django                       import forms
from django.core.exceptions       import ValidationError
from django.utils.translation     import gettext_lazy as _
from django.contrib.auth          import get_user_model, password_validation
from django.contrib.auth.forms    import UserChangeForm as BaseUserChangeForm, BaseUserCreationForm, UsernameField
from django.db.models             import Q

from phonenumber_field.formfields import PhoneNumberField

from .models import PendingUser
from .utils  import generate_otp_code, send_otp_code

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
        fields = ('username', 'phone_number', 'password')
        field_classes = {'username': UsernameField}

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
        model = PendingUser
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
        model = PendingUser
        fields = ["username", "phone_number", "password"]
        field_classes = {'username': UsernameField}

    def _post_clean(self):
        data = PendingUser.objects.filter(Q(username=self.cleaned_data.get('username')) | Q(phone_number=self.cleaned_data.get('phone_numebr')))
        if data.exists():
            data.delete()
        super()._post_clean()
        if User.objects.filter(phone_number__iexact=self.cleaned_data.get('phone_number')).exists():
            self.add_error("phone_number", "کاربر با این شماره تلفن وجود دارد ، لطفا شماره دیگری را امتحان کنید .")
    
    def save(self, commit):
        instance = super(UserPhoneNumberRegistrationForm, self).save(commit=False)
        otp = generate_otp_code()
        instance.otp_code = otp
        instance.password = self.cleaned_data.get('password')
        if commit:
            instance.save()
            send_otp_code(self.cleaned_data.get('phone_number'), otp)
        return instance


class OtpVerificationForm(forms.Form):
    otp = forms.CharField(required=True, label="کد فعال سازی")
    phone_number = PhoneNumberField(label="شماره تلفن", help_text="شماره تلفنی که کد فعال سازی به آن ارسال شد", required=True)

    def _post_clean(self):
        super()._post_clean()
        pending_user = PendingUser.objects.filter(
            phone_number=self.cleaned_data.get('phone_number'), 
            otp_code=self.cleaned_data.get('otp')
        ).first()
        self.cleaned_data['pending_user'] = pending_user
        if not pending_user:
            self.add_error('otp', 'کد فعال سازی یا شماره تلفن اشتباه وارد شده')
        elif not pending_user.is_valid():
            pending_user.delete()
            self.add_error('otp', 'کد فعال سازی منقضی شده است . لطفا مجددا ثبت نام نمایید')
    
    def create(self):
        otp = self.cleaned_data.pop('otp')
        pending_user = self.cleaned_data.pop('pending_user')
        user = User.objects.create_user_with_phone(username=pending_user.username, phone_number=pending_user.phone_number, password=pending_user.password)
        pending_user.delete()
        return user