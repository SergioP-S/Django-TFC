from django.contrib import admin
from .models import List, Item, Tag
from .forms import AddTagForm

class ListAdmin(admin.ModelAdmin):
      readonly_fields = ("created_on",) #setting some fields to readonly
admin.site.register(List, ListAdmin) #the model is registered into the admin panel

class ItemAdmin(admin.ModelAdmin):
      readonly_fields = ("added_on",) 
admin.site.register(Item, ItemAdmin) 

class TagAdmin(admin.ModelAdmin):
      form = AddTagForm #using the form to add a tag
      fieldsets = (
        (None, {
            'fields': (('name', 'color'),'list')
            }),
        )
admin.site.register(Tag, TagAdmin) #the model is registered into the admin panel