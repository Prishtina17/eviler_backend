import binascii
import json
import datetime

import django
import jwt
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
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
    permission_classes = [IsAuthenticated]
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



@csrf_exempt
@api_view(("POST",))
@permission_classes([IsAuthenticated])
def check_nft(request):
    endpoint = settings.QUICKNODE_ENDPOINT
    response = JWTAuthentication().authenticate(request)
    public_key = response[0].public_key
    payload = json.dumps({
        "id": 67,
        "jsonrpc": "2.0",
        "method": "qn_fetchNFTs",
        "params": {
            "wallet": f"{public_key}",
            "perPage": 40
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'x-qn-api-version': '1'
    }
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    print(json.loads(response.text)["result"]["totalItems"])
    for coll in json.loads(response.text)["result"]["assets"]:
        if coll["collectionName"] == settings.NFT_COLLECTION_NAME:
            return Response({"response":"successs"})
    return Response({"response":"nft did not found"})


@csrf_exempt
@api_view(("POST",))
@permission_classes([IsAuthenticated])
def check_transaction_commitment(request):
    if request.method == "POST":
        raw_sigs = [
            "5VERv8NMvzbJMEkV8xnrLkEaWRtSz9CosKDYjCJjBRnbJLgp8uirBgmQpjKhoR4tjF3ZpRzrFmBV6UjKdiSZkQUW",
            "5j7s6NiJS3JAkvgkoc18WVAsiSaci2pxB2A6ueCJP4tprA2TFg9wSyTLeYouxPBJEMzJinENTkpA52YStRW5Dia7"]
        data = json.loads(request.body)
        transaction_public_key = data.get("transaction_public_key")
        print(transaction_public_key)
        rpc_nodes = settings.SOLANA_RPC_NODES
        for rpc_node in rpc_nodes:
            print(rpc_node)
            client = Client(rpc_node)
            if client.is_connected():
                print("penis")

                #a = client.get_signature_statuses(sigs)
                #t = client.get_transaction(Signature.from_string(transaction_public_key))
                #resp = client.get_signature_statuses([Signature.from_string(transaction_public_key)], search_transaction_history=True)
                #resp_value = resp.value[0]
                #print(resp)
                print(GetSignatureStatuses([Signature.default()]))
                print(GetSignatureStatuses([Signature.from_string(transaction_public_key)]))

            else:
                continue
        return Response({"error":"No rpc nodes available"})
    return HttpResponse(status=405)


class GenerateLicenseKeyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = JWTAuthentication().authenticate(request)
        public_key = response[0].public_key
        data = json.loads(request.body)
        try:
            delta = relativedelta(months = data["month_delta"])
        except KeyError:
            delta = relativedelta(months=1)
        new_license = LicenseKey.objects.create(public_key, django.utils.timezone.now()+delta)
        new_license.save()
        return Response({"license_key":str(new_license.key)})

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
        except LicenseKey.DoesNotExist:
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
        print(request.body)
        response = JWTAuthentication().authenticate(request)

        return Response({"public_key":response[0].public_key})

    def post(self, request):
        print(request.body)

        response = JWTAuthentication().authenticate(request)

        return Response({"public_key": response[0].public_key})





