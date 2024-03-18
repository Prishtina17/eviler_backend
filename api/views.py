import binascii
import json

import django
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from django.contrib.auth import authenticate, login, user_logged_in
from rest_framework.views import APIView
from .serializers import EvilerTokenObtainPairSerializer

from solders.pubkey import Pubkey

from eviler import settings
from .models import EvilerUser, Module, News, Update
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
    def get(self, request):
        pass
class ListModules(APIView):

    def get(self, request):
        try:
            modules = Module.objects.all()
        except Module.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)



class ListNews(APIView):
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


"""def get_last_update(request):
    #if not request.user.is_authenticated:
    #    return HttpResponse(status=403)
    if request.method == "GET":
        try:
            last_update = Update.objects.last()
        except Update.DoesNotExist:
            return HttpResponse(status=404)
        file_handle = last_update.file.open()
        response = FileResponse(file_handle, content_type="file")
        response['Content-Length'] = last_update.file.size
        response['Content-Disposition'] = 'attachment; filename="%s.zip"' % last_update.Article

        return response"""


def discord_login(request):
    return redirect(AUTH_DISCORD_URL)


def discord_login_redirect(request):
    code = request.GET.get("code")
    user = exchange_code(code)
    request.META["discord_user"] = user
    eviler_user = authenticate(request)
    return JsonResponse(user)

@csrf_exempt
@permission_classes([AllowAny, ])
def solana_auth(request):
    if request.method == "POST":
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
            return JsonResponse({"response":data})
        except Exception as e:
            return Response(e)

    return HttpResponse(status=405)

@csrf_exempt
def ping(request):
    if request.method == "GET":
        return JsonResponse({"status":{request.user.is_authenticated}})



def exchange_code(code):
    data = {
        "client_id": str(CLIENT_ID),
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/api/login/redirect",
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    access_token = response.json()["access_token"]
    response = requests.get("https://discord.com/api/v10/users/@me", headers={
        "Authorization": "Bearer %s" % access_token
    })
    user = response.json()
    print(user)
    return user

