from django.core.validators import RegexValidator
from rest_framework import serializers
from authentication.models import User, Customer, Employee

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    contact_no = serializers.CharField(required=True, validators=[RegexValidator(regex=r'^(\+[0-9]{1,3})?[0-9]{10}$', message='Invalid Contact Number')])
    
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = ('contact_no', 'first_name',  'last_name', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CustomerSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    user = UserSerializer(required=True)
    address = serializers.CharField(max_length=250)


    class Meta:
        model = Customer
        fields = ('user', 'address')

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        password = user.pop('password', None)
        # as long as the fields are the same, we can just use this
        user_instance = User.objects.create(**user)

        instance = self.Meta.model(user=user_instance, **validated_data)
        instance.save()
        return instance