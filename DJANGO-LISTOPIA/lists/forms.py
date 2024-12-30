from django.forms import ModelForm, TextInput, CheckboxInput, Select
from .models import List, Item, Tag

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre de la lista', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción (opcional)', 'class': 'w-full p-2 border rounded'}),
            'is_public': CheckboxInput(attrs={'class': 'mr-2'}),
        }

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del item', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción (opcional)', 'class': 'w-full p-2 border rounded'}),
        }

class ModifyListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre de la lista', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción (opcional)', 'class': 'w-full p-2 border rounded'}),
            'is_public': CheckboxInput(attrs={'class': 'mr-2'}),
        }

class ModifyItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del item', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción (opcional)', 'class': 'w-full p-2 border rounded'}),
        }

class AddTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del tag', 'class': 'w-full p-2 border rounded'}),
            'color': Select(choices=[
                ('#FF0000', 'Rojo'),
                ('#00FF00', 'Verde'),
                ('#1980E6', 'Azul'),
                ('#FFFF00', 'Amarillo'),
                ('#FFA500', 'Naranja'),
                ('#FF80FF', 'Rosa'),
                ('#800080', 'Morado'),
                ('#00FFFF', 'Cian')
            ], attrs={'class': 'w-full p-2 border rounded'}),
        }