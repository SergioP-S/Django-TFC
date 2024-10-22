from django.contrib import admin
from .models import List, Item

class ListAdmin(admin.ModelAdmin):
      readonly_fields = ( "created_on", "last_modified") #Falta añadir el campo modified_by
admin.site.register(List, ListAdmin) #Se registra el modelo en el panel de administración

class ItemAdmin(admin.ModelAdmin):
      readonly_fields = ("added_on","last_modified") #setting some fields to readonly
admin.site.register(Item, ItemAdmin) #the model is registered into the admin panel