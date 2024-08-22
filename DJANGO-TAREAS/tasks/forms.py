from django.forms import ModelForm
from .models import Task

#formulatrio para crear tareas
class TaskForm(ModelForm):
    class Meta: 
        model = Task #modelo del que se obtienen los campos
        fields = ['title', 'description', 'important'] #Campos que tedrá el formulario