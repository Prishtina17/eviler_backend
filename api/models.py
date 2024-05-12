import uuid

import django
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.safestring import mark_safe
import eviler.settings as settings

# Create your models here.



class EvilerUserManager(UserManager):
    def create_user_from_public_key(self, public_key):
        new_user = self.create(
            username=public_key,
            public_key=public_key
        )
        return new_user



    def create_superuser(self, email,  username, password = None):
        user = self.create(username=username,public_key=username,email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user





class EvilerUser(AbstractUser):
    objects = EvilerUserManager()
    username = models.CharField(name="username", unique=True)
    password = models.CharField(name="password", null=True)
    email = models.EmailField(null=True)

    public_key = models.CharField(name="public_key", max_length=44, default="", unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return getattr(self, "public_key")


class ActiveSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    fingerprint = models.CharField(name="fingerprint", default="None",max_length=64)
    expiration = models.DateTimeField(name="expiration",default = django.utils.timezone.now)
    owner = models.ForeignKey("LicenseKey", name="owner", on_delete=models.CASCADE)

    def __str__(self):
        return getattr(self, "fingerprint") + "/" + str(getattr(self, "expiration"))

class LicenseKeyManager(models.Manager):
    def create(self, public_key, nft_address,renewalExpiration=None, sessions_limit=settings.DEFAULT_SESSIONS_LIMIT):
        key = uuid.uuid4()
        return super().create(owner=EvilerUser.objects.get(public_key=public_key),
                              key=key,
                              nftAddress=nft_address,
                              renewalExpiration=renewalExpiration,
                              sessionsLimit = sessions_limit)
class LicenseKey(models.Model):
    objects = LicenseKeyManager()
    owner = models.ForeignKey(EvilerUser, name="owner",  null=True,on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4(), unique=True)
    sessionsLimit = models.PositiveIntegerField(name="sessionsLimit", default=settings.DEFAULT_SESSIONS_LIMIT)
    renewalExpiration = models.DateTimeField(name="renewalExpiration", default=django.utils.timezone.now, null = True)
    nft_address = models.CharField(name="nftAddress", null=True, unique=True,max_length=64)
    def __str__(self):
        return str(getattr(self, "key")) + "/" + str(getattr(self,"owner"))

"""class ActiveModule(models.Model):
    module = models.ForeignKey(Module, db_index=True, on_delete=models.PROTECT,null=True)
    expired_data = models.DateTimeField(default=django.utils.timezone.now)
    owner = models.ForeignKey(EvilerUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(getattr(self, "owner"))+"/"+str(getattr(self, "module"))"""



