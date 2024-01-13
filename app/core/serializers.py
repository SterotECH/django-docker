from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from core import models
from core.signals import user_created
User = get_user_model()
UserModel = models.User

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
        fields = ['id', 'username', 'email', 'first_name','last_name', 'user_type', 'password']

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
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'user_type',
            'email'
        ]


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=68,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField()
    password_confirm = serializers.CharField(
        max_length=68,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_token(self, value):
        try:
            reset_token = models.Reset.objects.get(token=value)
            user = User.objects.get(email=reset_token.email)
        except (models.Reset.DoesNotExist, User.DoesNotExist):
            raise serializers.ValidationError("Invalid token", code='404')

        self.reset_token = reset_token
        self.user = user
        return value

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def save(self):
        self.user.password = make_password(self.validated_data['password'])
        self.user.save()

        self.reset_token.delete()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
