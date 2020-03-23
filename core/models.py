from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.conf import settings



class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creating ans saving a new user"""
        if email is None or email == '':
            raise ValueError('email field is required')
        elif password is None:
            raise ValueError('password is required')
        else:
            user = self.model(
                email=self.normalize_email(email),
                **extra_fields
                )
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creating and saving a new superuser"""
        superuser = self.create_user(email, password)
        superuser.is_customer = False
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser

    def create_supervisor(self, email, password, **extra_fields):
        """Creating and saving a new supervisor"""
        supervisor = self.create_user(email, password)
        supervisor.is_customer = False
        supervisor.is_supervisor = True
        supervisor.is_staff = False
        supervisor.save(using=self._db)
        return supervisor

    def create_delivery_guy(self, email, password, **extra_fields):
        """Creating and saving a new delivery guy"""
        delivery_guy = self.create_user(email, password)
        delivery_guy.is_customer = False
        delivery_guy.is_delivery_guy = True
        delivery_guy.is_staff = False
        delivery_guy.save(using=self._db)
        return delivery_guy


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_supervisor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_delivery_guy = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Order(models.Model):
    """Customer's orders model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    seller_name = models.CharField(max_length=255)
    seller_phone = models.CharField(max_length=15)
    seller_location = models.URLField(max_length=200)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    customer_location = models.URLField(max_length=200)

    def __str__(self):
        return f'seller_name - {seller_name} \n seller_phone - {seller_phone} \n seller_location - {seller_location} \n customer_name - {customer_name} \n customer_phone - {customer_phone} \n customer_location - {customer_location}'
