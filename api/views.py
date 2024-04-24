import binascii
import json
import datetime

import django
import jwt
from asgiref.sync import sync_to_async, AsyncToSync
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from django.contrib.auth import authenticate, login, user_logged_in
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed, Processed
from solders.rpc.requests import GetSignatureStatuses
from solders.signature import Signature

from .check_nft import get_nfts
from .serializers import EvilerTokenObtainPairSerializer

from solders.pubkey import Pubkey

from eviler import settings
from .models import EvilerUser, Module, News, Update, LicenseKey, ActiveSession
from .serializers import EvilerUserSerializer, ModuleSerializer, NewsSerializer, UpdateSerializer
import requests
import base58
from nacl.signing import VerifyKey

AUTH_DISCORD_URL = "https://discord.com/api/oauth2/authorize?client_id=1180825238838181939&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Flogin%2Fredirect&scope=identify"
CLIENT_ID = 1180825238838181939
CLIENT_SECRET = "IoXkOHm4o1KBCBc6RrtZNc8HaTKainEv"


def get_user_data(request, user_id: int):
    print(request.user.id)
    print(request.user.is_authenticated)
    if request.user.is_authenticated and request.user.id == user_id:
        pass
    else:
        return HttpResponse(status=403)
    if request.method == "GET":
        user = None
        try:
            user = EvilerUser.objects.get(id = user_id)
        except EvilerUser.DoesNotExist:
            return HttpResponse(status=404)
        serializer = EvilerUserSerializer(user)
        return JsonResponse(serializer.data)

class DetailUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = EvilerUserSerializer(user).data
        return Response(data)
class ListModules(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            modules = Module.objects.all()
        except Module.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ModuleSerializer(modules, many=True)

        return Response(serializer.data)



class ListNews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            news = News.objects.all()
        except News.DoesNotExist:
            return HttpResponse(status=404)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)



class ListUpdates(APIView):
    def get(self, request):
        try:
            updates = Update.objects.all()
        except Update.DoesNotExist:
            return HttpResponse(status=404)
        serializer = UpdateSerializer(updates, many=True)
        return Response(serializer.data)




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
            serializer = EvilerTokenObtainPairSerializer(context= {"request":request})
            data = serializer.validate()
            return Response({"refresh": data["refresh"], "access": data["access"]})
        except Exception as e:
            return Response(e)


class CheckTransactionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        data = json.loads(request.body)
        print(request.user)
        client = Client("https://api.mainnet-beta.solana.com")
        sigs = client.get_signatures_for_address(Pubkey.from_string(str(request.user)))
        for sig in sigs.value:
            print(sig)
        return Response()
class CheckNftView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):

        response = JWTAuthentication().authenticate(request)
        public_key = response[0].public_key

        public_key = "DywvRGQzikkTfgakuh76WGKru7FWHX3HnFgS1CUGzGQt"

        nfts = get_nfts(public_key)
        if nfts != []:
            license_keys = []
            mints = []
            #Получает/генерирует лицензионные ключ на основе mint address полученных через rpc метод
            #Удаляет лицензионный ключ, владелец нфт которого поменялся, создаёт новый ключ для текущего владельца нфт
            for nft in nfts:
                mints.append(nft["mint"])
                try:
                    license_key = LicenseKey.objects.get(nftAddress = nft["mint"])
                    if license_key.owner != EvilerUser.objects.get(public_key = public_key):
                        license_key.delete()
                        license_key = LicenseKey.objects.create(public_key=public_key, nft_address=nft["mint"])
                    license_keys.append({license_key.key:nft})
                except ObjectDoesNotExist:
                    try:
                        license_keys.append({LicenseKey.objects.create(public_key=public_key, nft_address = nft["mint"]).key : nft})
                    except ObjectDoesNotExist:
                        EvilerUser.objects.create_user_from_public_key(public_key)
                        license_keys.append({LicenseKey.objects.create(public_key=public_key, nft_address = nft["mint"]).key : nft})


            return Response({"response":license_keys})


        return Response({"response": "no nft found"})


class ValidateKeyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        data = json.loads(request.body)
        key = data.get("license_key")
        if not key:
            return Response({"response" : "No license key passed"})
        fingerprint = data.get("fingerprint")
        if not fingerprint:
            return Response({"response" : "No fingerprint passed"})

        try:
            licensekey = LicenseKey.objects.get(key=key)
        except ObjectDoesNotExist:
            return Response({"response" : "Key does not exist"})
        if licensekey.renewalExpiration < django.utils.timezone.now():
            return Response({"response" : "License key expired"})
        active_sessions = ActiveSession.objects.filter(owner=licensekey)
        for active_session in active_sessions:
            if active_session.fingerprint == fingerprint:
                active_session.expiration += datetime.timedelta(minutes=5)
                active_session.save()
                return Response({"response": "Session was extended successfully"})

        if len(active_sessions) >= licensekey.sessionsLimit:
            return Response({"response" : "Sessions limit"})
        newActiveSession = ActiveSession.objects.create(fingerprint=fingerprint,
                                                                    expiration=django.utils.timezone.now() + datetime.timedelta(minutes=5),
                                                                    owner = licensekey)
        newActiveSession.save()
        return Response({"response": "New session was added"})

class PingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        response = JWTAuthentication().authenticate(request)

        return Response({"public_key":response[0].public_key})

    def post(self, request):

        response = JWTAuthentication().authenticate(request)

        return Response({"public_key": response[0].public_key})





