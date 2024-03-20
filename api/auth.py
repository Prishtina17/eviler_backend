import json

import base58
import jwt
from django.contrib.auth.backends import BaseBackend
from nacl.signing import VerifyKey
from rest_framework import authentication
from rest_framework_simplejwt.tokens import RefreshToken

from eviler import settings
from .models import EvilerUser, EvilerUserManager
from django.core.exceptions import ObjectDoesNotExist
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import EvilerUser

class SolanaAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        data = json.loads(request.body)
        print("huy")
        public_key_str = data.get('public-key')
        public_key = base58.b58decode(public_key_str)

        signature = data.get('signature')
        msg = data.get('msg')
        msg = bytes(msg, "utf-8")
        signature = base58.b58decode(signature)

        try:
            result = VerifyKey(public_key).verify(smessage=msg, signature=signature)
        except Exception as e:
            print(e)
            return (None,None)
        user = None
        try:
            user = EvilerUser.objects.get(public_key=public_key_str)
        except ObjectDoesNotExist:
            user = EvilerUser.objects.create_user_from_public_key(public_key_str)



        return (user, None)
