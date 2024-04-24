import uuid

import django
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.

class Module(models.Model):
    name = models.CharField(name="Module Name", max_length=100)
    def __str__(self):
        return getattr(self, "Module Name")

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
    def create(self, public_key, nft_address,renewalExpiration=None,):
        key = uuid.uuid4()
        return super().create(owner=EvilerUser.objects.get(public_key=public_key),

                              key=key,
                              nftAddress=nft_address)
class LicenseKey(models.Model):
    objects = LicenseKeyManager()
    owner = models.ForeignKey(EvilerUser, name="owner",  null=True,on_delete=models.CASCADE)
    key = models.CharField(name="key",max_length=64, default=uuid.uuid4(), unique=True)
    sessionsLimit = models.PositiveIntegerField(name="sessionsLimit", default=5)
    renewalExpiration = models.DateTimeField(name="renewalExpiration", default=django.utils.timezone.now)
    nft_address = models.CharField(name="nftAddress", null=True, unique=True,max_length=64)
    def __str__(self):
        return getattr(self, "key") + "/" + str(getattr(self,"renewalExpiration"))

"""class ActiveModule(models.Model):
    module = models.ForeignKey(Module, db_index=True, on_delete=models.PROTECT,null=True)
    expired_data = models.DateTimeField(default=django.utils.timezone.now)
    owner = models.ForeignKey(EvilerUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(getattr(self, "owner"))+"/"+str(getattr(self, "module"))"""



class ImageModel(models.Model):
    image = models.ImageField(name="Image")


class News(models.Model):
    article = models.CharField(name="Article", max_length=100, default="article")
    text = models.TextField(name="Text",default="text")
    images = models.ManyToManyField(ImageModel, name="Images", null=True)
    pub_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return getattr(self, "Article")

class Update(models.Model):
    article = models.CharField(name="Article",max_length=500, default="Article")
    pub_date = models.DateTimeField(default=django.utils.timezone.now)
    file = models.FileField(upload_to="uploads/updates/")

    def __str__(self):
        return getattr(self, "Article")

