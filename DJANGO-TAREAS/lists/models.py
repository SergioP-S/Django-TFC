from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    """
    Represents a list entity with a name, description, creator, collaborators, and timestamps.
    Attributes:
        name (CharField): The name of the list, with a maximum length of 50 characters.
        description (CharField): A brief description of the list, with a maximum length of 256 characters.
        creator (ForeignKey): A reference to the User who created the list. If the user is deleted, the list is also deleted.
        created_on (DateTimeField): The date and time when the list was created. Automatically set on creation.
        collaborators (ManyToManyField): A set of Users who are collaborators on the list. Can be blank.
        last_modified (DateTimeField): The date and time when the list was last modified. Automatically updated on modification.
        modified_by (ForeignKey): A reference to the User who last modified the list. Can be blank or null.
    Methods:
        __str__: Returns a string representation of the list, including its name and the username of its creator.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_lists")
    created_on = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(User, related_name="collaborated_lists", blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self): #método para mostrar el título cuando se quiera mostrar un registro, por ejemplo en el panel admin
        return self.name + ' - de ' + self.creator.username

class Item(models.Model):
  
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_items')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=256)
    added_on = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(null=False, default=False)
    last_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self): #método para mostrar el título cuando se quiera mostrar un registro, por ejemplo en el panel admin
        return self.name + ' - added by ' + self.added_by.username
    
class Tag(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=7, default="#007bff")
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - Lista: " + self.list.name