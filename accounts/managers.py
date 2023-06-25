from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user_with_phone(self, username, phone_number, password, **extra_fields):
        self.create_user(username=username, phone_number=phone_number, password=password, is_active=True, phone_number_verified=True, **extra_fields)
    
    def create_user_with_email(self, username, email, password, **extra_fields):
        self.create_user(username=username, email=email, password=password, is_active=True, email_verified=True, **extra_fields)
    
    def create_superuser(self, username, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, phone_number, password, **extra_fields)