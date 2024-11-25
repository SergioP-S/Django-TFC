from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("likes",) 
admin.site.register(Profile, ProfileAdmin)