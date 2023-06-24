from django.contrib.auth.models    import AbstractBaseUser
from django.db                     import models
from django.utils.translation      import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser):
    phone_number = PhoneNumberField(_("شماره تلفن"), unique=True)
    email = models.EmailField(_("آدرس ایمیل"), blank=True, null=True, unique=True)
    full_name = models.CharField(_("نام و نام خانوادگی"), max_length=60, blank=True, null=True)

    is_active = models.BooleanField(_("فعال"), default=True)
    is_admin = models.BooleanField(_("ادمین"), default=False)
    date_joined = models.DateTimeField(_("تاریخ ثبت نام"), auto_now_add=True)

    email_verfied = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = ['email']


    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True
    
    def __str__(self):
        return self.phone_number


class OtpCode(models.Model):
    phone_number = PhoneNumberField(_("شماره تلفن"))
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
    
    class Meta:
        verbose_name = _("کد فعال سازی")
        verbose_name_plural = _("کد های فعال سازی")