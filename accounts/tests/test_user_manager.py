from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UserManagerTestCase(TestCase):
    def test_user_create(self):
        User = get_user_model()
        user = User.objects.create(
            phone_number="09024978823",
            email="ad.kiany.2009@gmail.com",
            username="abdolrahman",
            password="thisisapass"
        )
        self.assertEqual(user.phone_number, "09024978823")
        self.assertEqual(user.phone_number.as_e164, "+989024978823")
        self.assertEqual(user.email, "ad.kiany.2009@gmail.com")
        self.assertEqual(user.username, "abdolrahman")
        self.assertFalse(user.email_verfied)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.phone_number_verified)
        self.assertFalse(user.is_active)
    
    def test_superuser_create(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="abdolrahman",
            phone_number="09024978823",
            password="thisisapass",
            email="ad.kiany.2009@gmail.com",
        )
        self.assertEqual(admin_user.phone_number, "09024978823")
        self.assertEqual(admin_user.phone_number.as_e164, "+989024978823")
        self.assertEqual(admin_user.email, "ad.kiany.2009@gmail.com")
        self.assertEqual(admin_user.username, "abdolrahman")
        self.assertFalse(admin_user.email_verfied)
        self.assertFalse(admin_user.phone_number_verified)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_active)
