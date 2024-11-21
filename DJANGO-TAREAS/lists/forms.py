from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import List, Item, Tag


class ListForm(ModelForm):
    class Meta: 
        model = List #modelo where fields are obtained
        fields = ['name', 'description'] #fields shown in the form

class NewItemForm(ModelForm):
    class Meta: 
        model = Item
        fields = ['name', 'description']

#Form to set an item as done
class ItemStatusForm(ModelForm):
    class Meta:
        model = Item
        fields = ['is_done']

class ModifyListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name', 'description'] #¿Añadir nombre de la lista, se puede modificar ?

class ModifyItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']

class AddTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }