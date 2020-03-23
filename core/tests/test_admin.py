from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='aim@opsdev.ai',
            password='test_12323'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='aim@gmail.com',
            password='test_create_superuser',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are lidted on the user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        self.assertTrue(self.user.check_password('test_create_superuser'))

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_page(self):
        """Test that the create user works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
