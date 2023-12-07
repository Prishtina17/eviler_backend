from django.contrib.auth.backends import BaseBackend
from rest_framework import authentication

from .models import EvilerUser, EvilerUserManager
from django.core.exceptions import ObjectDoesNotExist

class DiscordAuthenticationBackend(authentication.BaseAuthentication):
    def authenticate(self, request, user):
         find_user = None
         try:
             find_user = EvilerUser.objects.get(discord_id=user["id"])
             print(f"User was found: {find_user.id}")
             return (find_user, None)
         except ObjectDoesNotExist:
             print("User was not found. Creating a new one...")
             new_user = EvilerUser.objects.create_user_from_discord(user)
             new_user.save()
             return new_user


