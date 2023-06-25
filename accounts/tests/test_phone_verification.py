from django.test import TestCase
from accounts.models import PendingUser, User
from time import sleep

class PhoneRegisterTestCase(TestCase):
    def test_register(self):
        register_response = self.client.post(
            '/auth/register/phone_number/', 
            {
                "username": "root",
                "phone_number": "09023768475",
                "password": "kianish40",
                "password_repeat": "kianish40"
            }
        )
        pending_user = PendingUser.objects.filter(username="root")
        self.assertRedirects(register_response, '/auth/register/phone_number/verify/')
        self.assertTrue(pending_user.exists())
        self.assertEqual(pending_user.first().username, "root")
        self.assertEqual(pending_user.first().phone_number, "09023768475")
        verify_response = self.client.post(
            '/auth/register/phone_number/verify/', 
            {
                "phone_number": "09023768475",
                "otp": pending_user.first().otp_code
            }
        )
        self.assertRedirects(verify_response, '/auth/register/', status_code=302)
        user = User.objects.filter(username="root")
        self.assertTrue(user.exists())
        self.assertTrue(user.first().is_active)
        self.assertTrue(user.first().phone_number_verified)
        self.assertFalse(user.first().is_admin)
        self.assertFalse(user.first().email_verfied)
        self.assertEqual(user.first().phone_number, "09023768475")

        self.client.login(credentials=user)
    
    def test_user_otp_exp_time(self):
        register_response = self.client.post(
            '/auth/register/phone_number/', 
            {
                "username": "root",
                "phone_number": "09023768475",
                "password": "kianish40",
                "password_repeat": "kianish40"
            }
        )
        pending_user = PendingUser.objects.filter(username="root").first()
        self.assertTrue(pending_user.is_valid(0.01))
        sleep(0.6)
        self.assertFalse(pending_user.is_valid(0.01))
    
    def test_wrong_data_register(self):
        register_response = self.client.post(
            '/auth/register/phone_number/', 
            {
                "username": "",
                "phone_number": "09023768475",
                "password": "kianish40",
                "password_repeat": "kianish40"
            }
        )
        self.assertEqual(register_response.status_code, 400)