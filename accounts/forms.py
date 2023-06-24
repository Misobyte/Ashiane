from django                    import forms
from django.utils.translation  import gettext_lazy as _
from django.core.exceptions    import ValidationError
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, BaseUserCreationForm
from django.contrib.auth       import get_user_model, password_validation

from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()

class AdminUserCreationForm(BaseUserCreationForm):
    phone_number = PhoneNumberField(label="شماره تلفن")

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('phone_number', 'full_name')

class AdminUserChangeForm(BaseUserChangeForm):
    pass

class AdminUserRegistrationForm(forms.ModelForm):
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
        fields = ('phone_number',)

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