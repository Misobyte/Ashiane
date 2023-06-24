from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, OtpCode
from .forms import AdminUserCreationForm, AdminUserChangeForm

# Register your models here.

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "code", "created"]

class UserAdmin(admin.ModelAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "full_name", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "email", "full_name", "is_staff")

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)