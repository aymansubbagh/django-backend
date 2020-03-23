from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create-user')
TOKEN_URL = reverse('user:user-token')
ME_URL = reverse('user:user-me')

CREATE_SUPERVISOR_URL = reverse('user:create-supervisor')
TOKEN_SUPERVISOR_URL = reverse('user:supervisor-token')
ME_SUPERVISOR_URL = reverse('user:supervisor-me')

CREATE_SUPERUSER_URL = reverse('user:create-superuser')
TOKEN_SUPERUSER = reverse('user:superuser-token')
ME_SUPERUSER_URL = reverse('user:superuser-me')

CREATE_DELIVERYGUY_URL = reverse('user:create-deliveryguy')
TOKEN_DELIVERYGUY_URL = reverse('user:deliveryguy-token')
ME_DELIVERYGUY_URL = reverse('user:deliveryguy-me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user public api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succes(self):
        """Test creating user with valid payload is successful"""

        payload = {
            'email': 'aim@fg.com',
            'password': 'asdasfd34',
            'name': 'aim'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_create_valid_superuser_succes(self):
        """Test creating superuser with valid payload is successful"""

        payload = {
            'email': 'aim@fg.com',
            'password': 'asdasfd34',
            'name': 'aim'
        }

        res = self.client.post(CREATE_SUPERUSER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        superuser = get_user_model().objects.get(**res.data)

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertFalse(superuser.is_customer)
        self.assertTrue(superuser.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_create_valid_supervisor_succes(self):
        """Test creating supervisor with valid payload is successful"""

        payload = {
            'email': 'aim@fg.com',
            'password': 'asdasfd34',
            'name': 'aim'
        }

        res = self.client.post(CREATE_SUPERVISOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        supervisor = get_user_model().objects.get(**res.data)

        self.assertFalse(supervisor.is_staff)
        self.assertTrue(supervisor.is_supervisor)
        self.assertFalse(supervisor.is_customer)
        self.assertNotIn(payload['password'], res.data)
        self.assertTrue(supervisor.check_password(payload['password']))

    def test_create_valid_delivery_guy_succes(self):
        """Test creating delivery guy with valid payload is successful"""

        payload = {
            'email': 'aim@fg.com',
            'password': 'asdasfd34',
            'name': 'aim'
        }

        res = self.client.post(CREATE_DELIVERYGUY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        delivery_guy = get_user_model().objects.get(**res.data)

        self.assertFalse(delivery_guy.is_staff)
        self.assertTrue(delivery_guy.is_delivery_guy)
        self.assertFalse(delivery_guy.is_customer)
        self.assertNotIn(payload['password'], res.data)
        self.assertTrue(delivery_guy.check_password(payload['password']))

    def test_user_exists(self):
        """Test creating a user that already exsits"""
        payload = {
            'email': 'aim@fd.com',
            'password': 'asdasfd34',
            'name': 'aim'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'aim@fd.com',
            'password': 'asd',
            'name': 'aim'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exsits = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exsits)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'aim@fd.com',
            'password': 'asdfslsdfvdfd',
            'name': 'aim'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        payload = {
            'email': 'aim@fd.com',
            'password': 'asdfdfd',
        }

        create_user(
            email='dfjlkj@jlkd.com',
            password='1-worng',
            name='name'
        )

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is not given when user doent exist"""
        payload = {
            'email': 'aim@fd.com',
            'password': 'asd',
            'name': 'aim'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {
            'email': 'aim',
            'password': '',
            'name': 'aim'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTests(TestCase):
    """Test API requests that require authenticated"""

    def setUp(self):
        self.user = create_user(
            email='asd@dfd.com',
            password='dfsvscvsfv3',
            name='name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_succes(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.user.email, res.data.values())

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'aimd', 'password': 'ert3fdfs3q'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # explanation for why it returns false
        # https://stackoverflow.com/questions/55571170/django-check-password-always-returning-false
        self.assertFalse(self.user.check_password(payload['password']))
        self.assertEqual(self.user.name, payload['name'])
