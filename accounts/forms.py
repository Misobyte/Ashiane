from django                       import forms
from django.core.exceptions       import ValidationError
from django.utils.translation     import gettext_lazy as _
from django.contrib.auth          import get_user_model, password_validation
from django.contrib.auth.forms    import UserChangeForm as BaseUserChangeForm, BaseUserCreationForm
from django.contrib.auth.hashers  import make_password

from phonenumber_field.formfields import PhoneNumberField

from .models import PendingUser
from .utils  import generate_otp_code, send_otp_code

User = get_user_model()

class AdminUserCreationForm(BaseUserCreationForm):
    phone_number = PhoneNumberField(label="شماره تلفن")

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('phone_number', 'full_name')

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
        fields = ["phone_number", "full_name", "password"]
    
    def _post_clean(self):
        super()._post_clean()
        if User.objects.filter(phone__iexact=self.cleaned_data['phone_number']).exists():
            self.add_error("phone_number", "User with this phone number is Already exist")
    
    def save(self, commit):
        instance = super(UserPhoneNumberRegistrationForm, self).save(commit=False)
        otp = generate_otp_code()
        instance.otp_code = otp
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
            send_otp_code(self.cleaned_data['phone_number'], otp)
        return instance