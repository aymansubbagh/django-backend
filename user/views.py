from user.serializers import (UserSerializer, AuthTokenSerializer,
                              SuperuserSerializer, SupervisorSerializer,
                              DeliveryGuySerializer)

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateSuperuserView(generics.CreateAPIView):
    """Create a new superuser in the system"""
    serializer_class = SuperuserSerializer


class CreateSupervisorView(generics.CreateAPIView):
    """Create a new supervisoruser in the system"""
    serializer_class = SupervisorSerializer


class CreateDeliveryGuyView(generics.CreateAPIView):
    """Create a new delivery guy in the system"""
    serializer_class = DeliveryGuySerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        if self.request.user.is_customer:
            return self.request.user


class ManageSuperuserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated superuser"""
    serializer_class = SuperuserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get_object(self):
        """Retrieve and return authenticated superuser"""
        if self.request.user.is_superuser:
            return self.request.user


class ManageSupervisorView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated supervisor"""
    serializer_class = SupervisorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated supervisor"""
        if self.request.user.is_supervisor:
            return self.request.user


class ManageDeliveryGuyView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated delivery guy"""
    serializer_class = DeliveryGuySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated delivery guy"""
        if self.request.user.is_delivery_guy:
            return self.request.user
