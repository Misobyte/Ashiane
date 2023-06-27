from django.contrib.auth.models      import AbstractBaseUser
from django.contrib.auth.validators  import UnicodeUsernameValidator
from django.db                       import models
from django.utils.translation        import gettext_lazy as _
from django.utils                    import timezone
from django.conf                     import settings

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

from datetime import datetime

# Create your models here.


username_validator = UnicodeUsernameValidator()


class PendingUser(models.Model):
    AUTH_METHOD_CHOICES = (
        ("number", "شماره تلفن"),
        ("email", "ایمیل")
    )
    auth_method = models.CharField(max_length=6, choices=AUTH_METHOD_CHOICES, null=True)
    username = models.CharField(
        _("نام کاربری"),
        max_length=60,
        primary_key=True,
        help_text=_(
            _("حداکثر ۶۰ حرف و فقط حروف و اعداد و غیره.")
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone_number = PhoneNumberField(_("شماره تلفن"), blank=True, null=True, unique=True)
    email = models.EmailField(_("آدرس ایمیل"), blank=True, null=True, unique=True)
    created_at = models.DateTimeField(_("تاریخ ثبت"), auto_now_add=True)
    otp_code = models.CharField(max_length=8, null=True)
    password = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "کاربر در انتظار"
        verbose_name_plural = "کاربران در انتظار"

    def __str__(self):
        return f"{str(self.phone_number)} {self.otp_code}"
    
    def is_valid(self, exp_time=settings.OTP_EXPIRE_TIME) -> bool:
        lifespan_in_seconds = float(exp_time * 60)
        now = datetime.now(timezone.get_current_timezone())
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

class User(AbstractBaseUser):
    username = models.CharField(
        _("نام کاربری"),
        max_length=60,
        primary_key=True,
        help_text=_(
            "Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone_number = PhoneNumberField(_("شماره تلفن"), unique=True, null=True, blank=True)
    email = models.EmailField(_("آدرس ایمیل"), blank=True, null=True, unique=True)

    is_active = models.BooleanField(_("فعال"), default=False)
    is_admin = models.BooleanField(_("ادمین"), default=False)
    date_joined = models.DateTimeField(_("تاریخ ثبت نام"), auto_now_add=True)

    email_verfied = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["phone_number"]


    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربران")
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True
    
    def __str__(self):
        return self.username
