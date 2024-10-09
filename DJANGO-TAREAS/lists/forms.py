from django.forms import ModelForm
from .models import List, Item

#formulatrio para crear Listas
class ListForm(ModelForm):
    class Meta: 
        model = List #modelo del que se obtienen los campos
        fields = ['name', 'description'] #Campos que tedrá el formulario

class NewItemForm(ModelForm):
    class Meta: 
        model = Item #modelo del que se obtienen los campos
        fields = ['name', 'quantity', 'weight'] #Campos que tedrá el formulario

#Form to set an item as done
class ItemStatusForm(ModelForm):
    class Meta:
        model = Item
        fields = ['is_done']