from django.forms import ModelForm, TextInput, CheckboxInput
from .models import List, Item, Tag

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre de la lista', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción', 'class': 'w-full p-2 border rounded'}),
            'is_public': CheckboxInput(attrs={'class': 'mr-2'}),
        }

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del item', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción', 'class': 'w-full p-2 border rounded'}),
        }

class ModifyListForm(ModelForm):
    class Meta:
        model = List
        fields = ['description', 'is_public']
        widgets = {
            'description': TextInput(attrs={'placeholder': 'Descripción', 'class': 'w-full p-2 border rounded'}),
            'is_public': CheckboxInput(attrs={'class': 'mr-2'}),
        }

class ModifyItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del item', 'class': 'w-full p-2 border rounded'}),
            'description': TextInput(attrs={'placeholder': 'Descripción', 'class': 'w-full p-2 border rounded'}),
        }

class AddTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del tag', 'class': 'w-full p-2 border rounded'}),
            'color': TextInput(attrs={'type': 'color', 'class': 'w-full p-2 border rounded'}),
        }