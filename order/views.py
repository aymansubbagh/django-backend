from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, authentication, permissions

from core.models import Order

from order import serializers


class CreateOrder(generics.CreateAPIView):
    """Create user's Orders in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.OrderSerializer



class ManageOrderView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage the orders list for the authenticated user"""
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Order.objects.all()

    def get_queryset(self):
        """ get the user's orders"""
        return self.queryset.filter(user=self.request.user).order_by('-seller_name')


class SupervisorOrderManage(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage all the customer's orders for the authenticated supervisor"""
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Order.objects.all()

    def get_queryset(self):
        """Shows all the orders for the supervisor"""
        if self.request.user.is_supervisor:
            return self.queryset
