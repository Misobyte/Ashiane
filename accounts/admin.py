from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, PendingUser
from .forms import AdminUserCreationForm, AdminUserChangeForm

# Register your models here.

@admin.register(PendingUser)
class PendingUserAdmin(admin.ModelAdmin):
    list_display = ["username", "otp_code", "phone_number", "created_at", "is_valid"]

class UserAdmin(admin.ModelAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "username", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "phone_number", "email", "is_staff")

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