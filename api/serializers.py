from rest_framework import serializers
from .models import EvilerUser,  Module, News, Update


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

"""class ActiveModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveModule
        fields = ["module", "expired_data"]"""


class EvilerUserSerializer(serializers.ModelSerializer):
   active_modules = serializers.SerializerMethodField()

   class Meta:
       model = EvilerUser
       fields = ["id", "Discord", "active_modules"]

   def get_active_modules(self, obj):
       """active_modules = ActiveModule.objects.filter(owner=obj)
       return ActiveModuleSerializer(active_modules, many=True).data"""
       return None

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = "__all__"