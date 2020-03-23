from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email="aim@ai.op", password='test_12323'):
    return get_user_model().objects.create_user(email, password)

def sample_order():
    return models.Order.objects.create(
        user = simple_user(),
        seller_name='miss haifa',
        seller_phone='0503410987',
        seller_location='https://goo.gl/maps/DKBH5uEAH5Sw7FVX6',
        customer_name='miss maha',
        customer_phone='050341341',
        customer_location='https://g.page/Goldencafe2?share',

    )

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating user with email successful"""
        email = "aim@devops.ai"
        password = "Test_12345"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_customer)

    def test_new_user_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'AIM@DEVOPS.AI'
        password = 'test_12323'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertIn(email.split('@')[-1].lower(), user.email)
        self.assertEqual(
            user.email,
            email.split('@')[0] + '@' + email.split('@')[-1].lower()
            )
        self.assertTrue(user.is_customer)

    def test_create_supervisor(self):
        """Test creating a new supervisor"""
        user = get_user_model().objects.create_supervisor(
            email='aim@dev.ai',
            password='test_12323'
        )

        self.assertFalse(user.is_customer)
        self.assertTrue(user.is_supervisor)

    def test_create_delivery_guy(self):
        """Test creating a new delivery guy"""
        user = get_user_model().objects.create_delivery_guy(
            email='aim@dev.ai',
            password='test_12323'
        )

        self.assertFalse(user.is_customer)
        self.assertTrue(user.is_delivery_guy)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='aim@dev.ai',
            password='test_12323'
        )

        self.assertFalse(user.is_customer)
        self.assertTrue(user.is_superuser)

    def test_new_superuser_invalid_email(self):
        """Test creating user with no email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(None, 'test_12323')

    def test_new_superuser_empty_password(self):
        """Test creating superuser with no password raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser('AIM@DEVOPS.AI', None)

    def test_new_supervisor_invalid_email(self):
        """Test creating supervisor with no email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_supervisor(None, 'test_12323')

    def test_new_supervisor_empty_password(self):
        """Test creating supervisor with no password raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_supervisor('AIM@DEVOPS.AI', None)

    def test_new_delivery_guy_invalid_email(self):
        """Test creating delivery guy with no email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_delivery_guy(None, 'test_12323')

    def test_new_delivery_guy_empty_password(self):
        """Test creating delivery guy with no password raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_delivery_guy('AIM@DEVOPS.AI', None)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test_12323')

    def test_new_user_empty_password(self):
        """Test creating user with no password raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('AIM@DEVOPS.AI', None)

    def test_order_model(self):
        """ Test that order is created"""
        order = models.Order.objects.create(
            user = sample_user(),
            seller_name='miss haifa',
            seller_phone='0503410987',
            seller_location='https://goo.gl/maps/DKBH5uEAH5Sw7FVX6',
            customer_name='miss maha',
            customer_phone='050341341',
            customer_location='https://g.page/Goldencafe2?share',

        )

        self.assertEqual(order.user.email, 'aim@ai.op')
        self.assertEqual(order.seller_name, 'miss haifa')
        self.assertEqual(order.seller_phone, '0503410987')
        self.assertEqual(order.seller_location, 'https://goo.gl/maps/DKBH5uEAH5Sw7FVX6')
        self.assertEqual(order.customer_name, 'miss maha')
        self.assertEqual(order.customer_phone, '050341341')
        self.assertEqual(order.customer_location, 'https://g.page/Goldencafe2?share')
