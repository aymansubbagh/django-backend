from rest_framework import serializers, status

from core.models import Order, User


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for the orders objects"""

    class Meta:
        model = Order
        fields = ('id', 'user', 'seller_name', 'seller_phone',
                  'seller_location', 'customer_name',
                  'customer_phone', 'customer_location',)
        read_only_fields = ('id',)
    def create(self, validated_data):
        """Cusotmers can only create a new order"""
        if User.objects.get(pk=validated_data['user'].id).is_customer:
            return Order.objects.create(**validated_data)
