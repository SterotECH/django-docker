from django.core.mail import EmailMessage
from django.conf import settings
from core.models import User
from rest_framework import exceptions, authentication

import threading

import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            _id = decode_access_tokens(token)

            user = User.objects.get(pk=_id)
            print(user)
            return (user, None)

        raise exceptions.AuthenticationFailed('unauthenticated')

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


def decode_access_tokens(token:str)-> int:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Access token expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid access token')


def decode_refresh_tokens(token:str)-> int:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Refresh token expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid refresh token')
