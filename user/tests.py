from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model

from user.utils import send_activation_email


class UserAccountTests(TestCase):

    def test_send_email(self):
        db = get_user_model()
        user = db.objects.create_user(
            'test@gmail.com', 'username', 'firstname', 'password'
        )

        send_activation_email(user, None)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Activate your account')

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'username', 'firstname', 'password'
        )
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'username')
        self.assertEqual(super_user.first_name, 'firstname')

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)

        self.assertEqual(str(super_user), "username")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', user_name='username', first_name='firstname', password='password', is_staff=False
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', user_name='username', first_name='firstname', password='password', is_superuser=False
            )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'firstname', 'password'
        )
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.user_name, 'username')
        self.assertEqual(user.first_name, 'firstname')

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_email_verified)
        self.assertFalse(user.is_active)

        self.assertEqual(str(user), "username")

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', user_name='a', first_name='firstname', password='password'
            )
        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='testuser@user.com', user_name='', first_name='firstname', password='password'
            )
