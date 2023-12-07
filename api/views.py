from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from django.contrib.auth import authenticate,login
from .models import EvilerUser, Module, News, Update
from .serializers import EvilerUserSerializer, ModuleSerializer, NewsSerializer, UpdateSerializer
import requests

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


def get_modules(request):
    if request.method == "GET":
        try:
            modules = Module.objects.all()
        except Module.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ModuleSerializer(modules, many=True)
        return JsonResponse(serializer.data, safe=False)


def get_next_news(request, current_last_new_id):
    #if not request.user.is_authenticated:
    #    return HttpResponse(status=403)
    if request.method == "GET":
        current_last_new_id = int(current_last_new_id)
        try:
            last_new_id = News.objects.last().id
            next_news = News.objects.filter(id__range=(current_last_new_id+1, last_new_id))
        except News.DoesNotExist:
            return HttpResponse(status=404)
        for new in next_news:
            print(new.id)
        print(next_news)
        serializer = NewsSerializer(next_news, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)


def get_last_update(request):
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

        return response


def discord_login(request):
    return redirect(AUTH_DISCORD_URL)


def discord_login_redirect(request):
    code = request.GET.get("code")
    user = exchange_code(code)
    eviler_user, auth = authenticate(request,user=user)
    print(eviler_user.is_authenticated)
    print(eviler_user.id)
    return JsonResponse(user)


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

class UserViewSet(viewsets.ModelViewSet):
   serializer_class = EvilerUserSerializer

   def get_user(self):
       user_id = self.kwargs['user_id']
       return EvilerUser.objects.filter(id=user_id)