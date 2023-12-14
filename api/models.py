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
    def create_user_from_discord(self, user):
        new_user = self.create(
            discord_id=user["id"],
            discord=user["username"]
        )
        return new_user


class EvilerUser(AbstractUser):
    objects = EvilerUserManager()
    discord = models.CharField(name="discord",max_length=100)
    discord_id = models.CharField(name="discord_id",default="", max_length=100)
    email = models.EmailField()
    license_key = models.ForeignKey("LicenseKey",name="licenseKey", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return getattr(self, "discord")


class ActiveSession(models.Model):
    fingerprint = models.CharField(name="fingerprint", default="None",max_length=64)
    expiration = models.DateTimeField(name="expiration",default = django.utils.timezone.now)
    owner = models.ForeignKey("LicenseKey", name="owner", on_delete=models.CASCADE)

    def __str__(self):
        return getattr(self, "fingerprint") + "/" + str(getattr(self, "expiration"))

class LicenseKey(models.Model):
    key = models.CharField(max_length=64, default="None")
    sessionsLimit = models.PositiveIntegerField(name="sessionsLimit", default=5)
    renewalExpiration = models.DateTimeField(name="renewalExpiration", default=django.utils.timezone.now)
    #activeSessions = models.ForeignKey(ActiveSession, name="activeSessions", on_delete=models.CASCADE)

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
    images = models.ManyToManyField(ImageModel, name="Images")
    pub_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return getattr(self, "Article")

class Update(models.Model):
    article = models.CharField(name="Article",max_length=500, default="Article")
    pub_date = models.DateTimeField(default=django.utils.timezone.now)
    file = models.FileField(upload_to="uploads/updates/")

    def __str__(self):
        return getattr(self, "Article")

