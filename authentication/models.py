from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_superuser(self, contact_no, first_name, password, **other_fields):

        other_fields.setdefault('is_employee', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_customer', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(contact_no, first_name, password, **other_fields)

    def create_user(self, contact_no, first_name, password, **other_fields):

        if not contact_no:
            raise ValueError(_('You must provide contact number'))

        user = self.model(contact_no=contact_no, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    is_superuser = models.BooleanField('admin', default=False)
    is_customer = models.BooleanField('customer', default=True)
    is_employee = models.BooleanField('employee', default=False)
     
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=True)
    contact_no = models.CharField(unique=True, max_length=14, validators=[RegexValidator(regex=r'^(\+[0-9]{1,3})?[0-9]{10}$', message='Invalid Contact Number')])
    email = models.EmailField()
    USERNAME_FIELD = 'contact_no'
    REQUIRED_FIELDS = ['first_name']
    
    # TODO: add orders and address
    objects  =  CustomUserManager()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=250)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    count = models.IntegerField()
