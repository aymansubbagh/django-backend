from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Order

from order.serializers import OrderSerializer

ORDER_URL = reverse('order:order-list')


class PrivateOrderTests(TestCase):
    """Test for orders model"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'aim@ai.op',
            'test_12345667'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_order(self):
        Order.objects.create(
            user=self.user,
            seller_name='miss lina',
            seller_phone='0501234590',
            seller_location='https://goo.gl/maps/DKBH5uEAH5Sw7FVX6',
            customer_name='miss dana',
            customer_phone='0501035590',
            customer_location='https://goo.gl/maps/GXJ33PdEjoaD1p1u9',
        )
        Order.objects.create(
            user=self.user,
            seller_name='miss lina',
            seller_phone='0501234590',
            seller_location='https://goo.gl/maps/DKBH5uEAH5Sw7FVX6',
            customer_name='miss dana',
            customer_phone='0501035590',
            customer_location='https://goo.gl/maps/GXJ33PdEjoaD1p1u9',
        )

        res = self.client.get(ORDER_URL)

        orders = Order.objects.all().order_by('-seller_name')
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
