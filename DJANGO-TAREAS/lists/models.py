from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=User)
def remove_user_from_collaborators(sender, instance, **kwargs):
    """
    Remove the user from all collaborators before the user is deleted.
    """
    # Remove the user from the collaborators of any lists
    lists_with_collaborator = List.objects.filter(collaborators=instance)
    for list in lists_with_collaborator:
        list.collaborators.remove(instance)
        print(f"Removed {instance.username} from collaborators of list {list.name}")

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
    is_public = models.BooleanField(default=False)
    

    def __str__(self): 
        return self.name + ' - de ' + self.creator.username

class Item(models.Model):
  
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_items')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=256, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self): #method to display the title when a record is shown, for example in the admin panel
        return self.name + ' - added by ' + self.added_by.username
    
class Tag(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=7, default="#007bff")
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - Lista: " + self.list.name