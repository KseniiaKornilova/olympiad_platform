from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'patronymic', 'email', 'status', 'degree']


class UserRegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name = validated_data['first_name'], 
            last_name = validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
