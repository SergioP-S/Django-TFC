from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    list_name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_lists")
    created_on = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(User, related_name="collaborated_lists", blank=True)

    def __str__(self): #método para mostrar el título cuando se quiera mostrar un registro, por ejemplo en el panel admin
        return self.list_name + ' - de ' + self.creator.username

class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=40)
    item_quantity = models.IntegerField(null=True, blank=True)
    item_weight = models.IntegerField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self): #método para mostrar el título cuando se quiera mostrar un registro, por ejemplo en el panel admin
        return self.item_name + ' - added by ' + self.added_by.username