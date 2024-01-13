import os
import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from rest_framework import generics, status, views, exceptions, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from core import models
from core import serializers
from core.utils import Util

User = get_user_model()


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]


class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse("core:email-verify")
        abs_url = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.username
            + " Use the link below to verify your email \n"
            + abs_url
        )

        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Activate your Account",
        }
        Util.send_email(data)

        messages.add_message(
            request,
            messages.SUCCESS,
            f"{user.name} created ${user.user_type} account successfully.",
        )
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = serializers.EmailVerificationSerializer

    def get(self, request: Request) -> Response:
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
            if not user.is_active:
                user.is_activate = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"]

        response = Response(
            {"access_token": serializer.data["tokens"]["access"]},
            status=status.HTTP_200_OK,
        )

        refresh_token = serializer.data["tokens"]["refresh"]

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="Lax",
            path="/api",
            expires=60 * 60 * 24 * 30,
            secure=True,
        )

        return response


class UserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request: Request):
        user_id = request.user.pk

        user = models.User.objects.get(pk=user_id)

        if user.is_authenticated:
            serialized_user = self.serializer_class(user)
            return Response(serialized_user.data)
        else:
            return Response(
                {"message": "Please authenticate first."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutAPIView(views.APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token", None)

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            raise exceptions.APIException("bad_token", status.HTTP_400_BAD_REQUEST)

        response = Response()
        response.delete_cookie("refresh_token")

        return Response(status=status.HTTP_204_NO_CONTENT)


class RefreshAPIView(views.APIView):
    def post(self, request) -> Response:
        refresh_token = request.COOKIES.get("refresh_token", None)

        try:
            # Check if the refresh token is valid and decode its payload
            payload = RefreshToken(refresh_token).payload

            # Blacklist the old refresh token
            RefreshToken(refresh_token).blacklist()

            # Generate a new access token and refresh token for the user
            user = User.objects.get(id=payload["user_id"])
            access_token = user.tokens()["access"]
            refresh_token = user.tokens()["refresh"]

            # Return the new access token in the response
            response = Response(
                {"access_token": access_token}, status=status.HTTP_200_OK
            )

            # Set the new refresh token in a cookie in the response
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="Lax",
                path="/api",
                expires=60 * 60 * 24 * 30,
                secure=True,
            )

            return response

        except (jwt.InvalidTokenError, TokenError):
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ForgotAPIView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetRequestSerializer  # Add this line

    def post(self, request):
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User with this email does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reset_token = default_token_generator.make_token(user)

        models.Reset.objects.update_or_create(
            email=email,
            defaults={'token': reset_token}
        )

        url = "http://localhost:3000/auth/reset/" + reset_token

        email_subject = "Reset Your Password"
        email_body = (
                'You have requested to reset your password\n<a href="%s">Click here to reset your password</a>\nIf you '  # noqa
                "did not make this request ignore this message" % url
        )
        to_email = (email,)
        data = {
            "email_body": email_body,
            "to_email": to_email,
            "email_subject": email_subject,
        }
        Util.send_email(data)
        return Response(
            {'detail': 'Password reset request successful. Check your email for instructions.'},  # noqa
            status=status.HTTP_200_OK
        )


class ResetAPIView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': 'Password reset successfully'},
            status=status.HTTP_200_OK
        )
