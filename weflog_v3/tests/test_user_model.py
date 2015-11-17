import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='hello')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='hello')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='hello')
        self.assertTrue(u.verify_password('hello'))

    def test_password_hashs_are_random(self):
        u1 = User(password='hello')
        u2 = User(password='hello')
        self.assertNotEqual(u1.password_hash, u2.password_hash)
