from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class CustomUserTestCase(TestCase):
    def test_user_create(self):
        User = get_user_model()
        user = User.objects.create(
            phone_number="09024978823",
            email="ad.kiany.2009@gmail.com",
            full_name="abdolrahman kiany",
            password="thisisapass"
        )
        self.assertEqual(user.phone_number, "09024978823")
        self.assertEqual(user.phone_number.as_e164, "+989024978823")
        self.assertEqual(user.email, "ad.kiany.2009@gmail.com")
        self.assertEqual(user.full_name, "abdolrahman kiany")
        self.assertFalse(user.email_verfied)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.phone_number_verified)
        self.assertTrue(user.is_active)
    
    def test_superuser_create(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            phone_number="09024978823",
            email="ad.kiany.2009@gmail.com",
            full_name="abdolrahman kiany",
            password="thisisapass"
        )
        self.assertEqual(admin_user.phone_number, "09024978823")
        self.assertEqual(admin_user.phone_number.as_e164, "+989024978823")
        self.assertEqual(admin_user.email, "ad.kiany.2009@gmail.com")
        self.assertEqual(admin_user.full_name, "abdolrahman kiany")
        self.assertFalse(admin_user.email_verfied)
        self.assertFalse(admin_user.phone_number_verified)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_active)