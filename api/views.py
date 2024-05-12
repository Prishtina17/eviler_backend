import json
import datetime

import django

from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.http import HttpResponse, JsonResponse, FileResponse

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from solana.rpc.api import Client

from .check_nft import moralis_get_nft
from .serializers import EvilerTokenObtainPairSerializer

from solders.pubkey import Pubkey

from eviler import settings
from .models import EvilerUser, LicenseKey, ActiveSession
from .serializers import EvilerUserSerializer
import requests
import base58
from nacl.signing import VerifyKey


class SolanaAuthView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = json.loads(request.body)

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
            return Response(e)
        user = None
        try:
            user = EvilerUser.objects.get(public_key=public_key_str)
        except ObjectDoesNotExist:
            user = EvilerUser.objects.create_user_from_public_key(public_key_str)

        try:
            serializer = EvilerTokenObtainPairSerializer(context={"request": request})
            data = serializer.validate()
            return Response({"refresh": data["refresh"], "access": data["access"]})
        except Exception as e:
            return Response(e)


"""class CheckTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = json.loads(request.body)
        print(request.user)
        client = Client("https://api.mainnet-beta.solana.com")
        sigs = client.get_signatures_for_address(Pubkey.from_string(str(request.user)))
        for sig in sigs.value:
            print(sig)
        return Response()"""


class CheckNftView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):

        public_key = str(request.user)
        #public_key = "DywvRGQzikkTfgakuh76WGKru7FWHX3HnFgS1CUGzGQt"

        nfts_metadata = moralis_get_nft(public_key)
        if nfts_metadata != []:
            license_keys = []
            mints = []
            # Получает/генерирует лицензионные ключ на основе mint address полученных через rpc метод
            # Удаляет лицензионный ключ, владелец нфт которого поменялся, создаёт новый ключ для текущего владельца нфт
            for nft in nfts_metadata:
                print(nft)
                print(type(nft))

                mints.append(nft["mint"])
                try:
                    license_key = LicenseKey.objects.get(nftAddress=nft["mint"])
                    if license_key.owner != EvilerUser.objects.get(public_key=public_key):
                        license_key.delete()
                        license_key = LicenseKey.objects.create(public_key=public_key, nft_address=nft["mint"])
                    license_keys.append({str(license_key.key): nft})
                except LicenseKey.DoesNotExist:
                    try:
                        license_keys.append(
                            {str(LicenseKey.objects.create(public_key=public_key, nft_address=nft["mint"])).key: nft})
                    except LicenseKey.DoesNotExist:
                        EvilerUser.objects.create_user_from_public_key(public_key)
                        license_keys.append(
                            {str(LicenseKey.objects.create(public_key=public_key, nft_address=nft["mint"])).key: nft})

            return Response({"response": license_keys})

        return Response({"response": "no nft found"})


# На данный момент логика expiration для license_key выключена
class ValidateKeyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = json.loads(request.body)
        key = data.get("license_key")
        if not key:
            return Response({"response": "No license key passed"})

        sessions_limit = data.get("sessions_limit")
        if not sessions_limit:
            sessions_limit = settings.DEFAULT_SESSIONS_LIMIT

        fingerprint = data.get("fingerprint")
        if not fingerprint:
            return Response({"response": "No fingerprint passed"})

        try:
            licensekey = LicenseKey.objects.get(key=key)
        except ObjectDoesNotExist:
            return Response({"response": "Key does not exist"})

        # if licensekey.renewalExpiration < django.utils.timezone.now():
        #    return Response({"response" : "License key expired"})

        active_sessions = ActiveSession.objects.filter(owner=licensekey)
        for active_session in active_sessions:
            if active_session.fingerprint == fingerprint:
                active_session.expiration += datetime.timedelta(minutes=5)
                active_session.save()
                return Response({"response": "Session was extended successfully"})

        if len(active_sessions) >= licensekey.sessionsLimit:
            return Response({"response": "Sessions limit"})
        newActiveSession = ActiveSession.objects.create(fingerprint=fingerprint,
                                                        expiration=django.utils.timezone.now() + datetime.timedelta(
                                                            minutes=5),
                                                        owner=licensekey,
                                                        sessions_limit=sessions_limit)
        newActiveSession.save()
        return Response({"response": "New session was added"})


class PingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = JWTAuthentication().authenticate(request)

        return Response({"public_key": response[0].public_key})

    def post(self, request):
        response = JWTAuthentication().authenticate(request)

        return Response({"public_key": response[0].public_key})
