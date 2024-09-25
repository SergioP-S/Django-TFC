from django.db import models
#from auth_app.models import CustomUser
from django.contrib.auth.models import User

# Create your models here.

#Modelo de la clase Tareas
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self): #método para mostrar el título cuando se quiera mostrar un registro, por ejemplo en el panel admin
        return self.title + ' - de ' + self.user.username
