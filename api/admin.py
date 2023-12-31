from django.contrib import admin
from .models import *

class ActiveSessionInline(admin.TabularInline):
    model = ActiveSession
    extra = 0
"""class ActiveModuleInline(admin.TabularInline):
   model = ActiveModule
   extra = 0
"""
"""class CustomUserAdmin(admin.ModelAdmin):
   inlines = [ActiveModuleInline]"""

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ActiveSessionInline]

admin.site.register(Module)
#admin.site.register(ActiveModule)
#admin.site.register(EvilerUser, CustomUserAdmin)
admin.site.register(EvilerUser)
admin.site.register(LicenseKey, CustomUserAdmin)
admin.site.register(ActiveSession)
admin.site.register(ImageModel)
admin.site.register(News)
admin.site.register(Update)
