from django.core.validators import RegexValidator
from rest_framework import serializers
from authentication.models import User, Customer, Staff
from django.contrib.auth import authenticate
import django.core.exceptions as exceptions
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    contact_no = serializers.CharField(required=True, validators=[RegexValidator(regex=r'^(\+[0-9]{1,3})?[0-9]{10}$', message='Invalid Contact Number')])
    
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    
    @property
    def data(self):
        ret = super().data
        if User.objects.get(contact_no = ret['contact_no']).is_superuser:
            ret['type'] = "Admin"
        return ret
    class Meta:
        model = User
        fields = ('contact_no', 'first_name',  'last_name', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_instance = User.objects.create_superuser(validated_data.pop('contact_no', None),validated_data.pop('first_name', None), password, **validated_data)
        return user_instance

class CustomerSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    user = UserSerializer(required=True)
    address = serializers.CharField(max_length=250)
    
    @property
    def data(self):
        ret = super().data
        ret['type'] = "Customer"
        return ret

    class Meta:
        model = Customer
        fields = ('user', 'address')

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        password = user.pop('password', None)
        user.setdefault('is_customer', True)   
        
        # as long as the fields are the same, we can just use this
        user_instance = User.objects.create_user(user.pop('contact_no', None),user.pop('first_name', None), password, **user)
        instance = self.Meta.model(user=user_instance, **validated_data)
        instance.save()
        return instance
    
class StaffSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    user = UserSerializer(required=True)
    
    @property
    def data(self):
        ret = super().data
        ret['type'] = "Staff"
        return ret
    class Meta:
        model = Staff
        fields = ['user']

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        password = user.pop('password', None)
        user.setdefault('is_staff', True)   
        
        user_instance = User.objects.create_user(user.pop('contact_no', None),user.pop('first_name', None), password, **user)

        instance = self.Meta.model(user=user_instance, **validated_data)
        instance.save()
        return instance
class AuthCustomTokenSerializer(serializers.Serializer):
    contact_no = serializers.CharField(required=True, validators=[RegexValidator(regex=r'^(\+[0-9]{1,3})?[0-9]{10}$', message='Invalid Contact Number')])
    password = serializers.CharField()

    def validate(self, attrs):
        contact_no = attrs.get('contact_no')
        password = attrs.get('password')

        if contact_no and password:
            # Check if user sent email
            # if validateEmail(email_or_username):
            #     user_request = get_object_or_404(
            #         User,
            #         email=email_or_username,
            #     )

            #     email_or_username = user_request.username

            user = authenticate(contact_no=contact_no, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "contact_no" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs