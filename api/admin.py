from django.contrib import admin
from django.contrib.auth.models import User

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



#admin.site.register(ActiveModule)
#admin.site.register(EvilerUser, CustomUserAdmin)
admin.site.register(EvilerUser)
admin.site.register(LicenseKey, CustomUserAdmin)
admin.site.register(ActiveSession)

