import datetime

import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.

class Module(models.Model):
    name = models.CharField(name="Module Name", max_length=100)

    def __str__(self):
        return getattr(self, "Module Name")

class ActiveModule(models.Model):
    module = models.ForeignKey(Module, db_index=True, on_delete=models.NOT_PROVIDED,null=True)
    expired_data = models.DateTimeField()

    def __str__(self):

        return "huy"          #блять я себе яйца отрежу нахуй


class ActiveModulesGroup(models.Model):
    name = models.CharField(name="name", max_length=100,default="huy")
    active_modules = models.ManyToManyField(ActiveModule, name="Active Modules")

    def __str__(self):
        return "huy"     #тут тоже яйца отрежу

class CustomUser(AbstractUser):
    email = models.EmailField(name="Email Field")
    discord = models.CharField(name="Discord",max_length=100)
    active_modules_group = models.ForeignKey(ActiveModulesGroup, on_delete=models.CASCADE,null=True)
    active_module = models.ForeignKey(ActiveModule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email

class ImageModel(models.Model):
    image = models.ImageField(name="Image")



class News(models.Model):
    article = models.CharField(name="Article", max_length=100, default="article")
    text = models.TextField(name="Text",default="text")
    images = models.ManyToManyField(ImageModel, name="Images")
    pub_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return getattr(self, "Article")
