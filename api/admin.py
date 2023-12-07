from django.contrib import admin
from .models import *


class ActiveModuleInline(admin.TabularInline):
   model = ActiveModule
   extra = 0

class CustomUserAdmin(admin.ModelAdmin):
   inlines = [ActiveModuleInline]

admin.site.register(Module)
admin.site.register(ActiveModule)
admin.site.register(EvilerUser, CustomUserAdmin)
admin.site.register(ImageModel)
admin.site.register(News)
admin.site.register(Update)
