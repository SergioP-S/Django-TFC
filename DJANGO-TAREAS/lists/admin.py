from django.contrib import admin
from .models import List, Item

# Register your models here.
class ListAdmin(admin.ModelAdmin):
      readonly_fields = ("created_on",)
admin.site.register(List, ListAdmin) #Se registra el modelo en el panel de administración

class ItemAdmin(admin.ModelAdmin):
      readonly_fields = ("added_on",)
admin.site.register(Item, ItemAdmin) #Se registra el modelo en el panel de administración