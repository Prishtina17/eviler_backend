from typing import Optional, Type, Dict, Any, TypeVar

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken

from .auth import SolanaAuthentication
from .models import EvilerUser,  Module, News, Update




class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

"""class ActiveModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveModule
        fields = ["module", "expired_data"]"""


class EvilerUserSerializer(serializers.ModelSerializer):
   class Meta:
       model = EvilerUser
       fields = ["id", "public_key", "email"]



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = "__all__"


class EvilerTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class: Optional[Type[Token]] = None

    default_error_messages = {
        "no_active_account": ("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)



    def validate(self) -> Dict[Any, Any]:
        authenticate_kwargs = {}
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        auth = SolanaAuthentication()
        self.user = auth.authenticate(self.context['request'])[0]



        return {}

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return cls.token_class.for_user(user)  # type: ignore

class EvilerTokenObtainPairSerializer(EvilerTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self) -> Dict[str, str]:
        data = super().validate()

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class TokenObtainSlidingSerializer(EvilerTokenObtainSerializer):
    token_class = SlidingToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        token = self.get_token(self.user)

        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

