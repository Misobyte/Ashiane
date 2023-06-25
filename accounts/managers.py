from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user_with_phone(self, phone_number, password, **extra_fields):
        self.create_user(phone_number=phone_number, password=password, email=None, is_active=True, phone_number_verified=True, **extra_fields)
    
    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(phone_number, email, password, **extra_fields)