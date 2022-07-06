from sqlite3 import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
  def test_create_user(self):
    db = get_user_model()
    user = db.objects.create_user("+254728877619", "vicjuma9545@gmail.com")
    user.password = "vicjuma112"
    self.assertIsInstance(user, db)
    self.assertFalse(user.is_staff)
    self.assertFalse(user.password)
    self.assertEqual(user.email, 'vicjuma9545@gmail.com')
    self.assertEqual(user.phone_number, '+254728877619')
    
    with self.assertRaises(
      ValueError):
      db.objects.create_user(
        phone_number='+254728877619', email="")
      
    with self.assertRaises(
      ValueError):
      db.objects.create_user(
        phone_number="", email="vic@gmail.com")
      
  def test_create_user(self):
    db = get_user_model()
    super_user = db.objects.create_superuser(
      "+254728877619", "vicjuma9545@gmail.com")
    self.assertTrue(super_user.is_staff)
    self.assertTrue(super_user.is_superuser)
    self.assertTrue(super_user.is_active)
    self.assertTrue(super_user.is_verified)