from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from .models import User as ModelUser
from core.signals import user_created
User = get_user_model()
UserModel = ModelUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True,
        style={'input_type': 'password'}
    )
    contact = serializers.CharField(
        max_length=20, min_length=9,
        style={'input_type': 'tel'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'contact', 'user_type', 'password']

    def perform_create(self, user):
        user_created.send_robust(self.__class__, user=user)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=255, min_length=3,)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True,
        style={'input_type': 'password'}
    )
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user:UserModel = User.objects.get(username=obj['username'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['username', 'password','tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        filtered_user_by_username = User.objects.filter(username=username)
        user:UserModel = auth.authenticate(username=username, password=password)
        if filtered_user_by_username.exists() and filtered_user_by_username[0].auth_provider != 'email':
            raise serializers.ValidationError(
                error='Please continue your login using ' + filtered_user_by_username[0].auth_provider)

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('Account disabled, contact admin')
        if not user.is_verified:
            raise serializers.ValidationError('Email is not verified')

        return {
            'user': user,
            'username': user.username,
            'password': user.password,
            'tokens': user.tokens,
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name', 'last_name','user_type','email','contact']
