from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

class Profile(models.Model):
    """
    Profile model that extends the built-in User model with additional fields.
    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model.
        description (TextField): A text field for the user's profile description.
        pic (ImageField): An optional image field for the user's profile picture, 
                          which is uploaded to the 'profile_pics' directory.
    Methods:
        __str__(): Returns the username of the associated User.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(pre_save, sender=Profile)
def delete_old_pic(sender, instance, **kwargs):
    """
    Signal receiver function to delete the old profile picture file when a new one is uploaded.
    Args:
        sender (Model class): The model class that sent the signal.
        instance (Model instance): The instance of the model that is being saved.
        **kwargs: Additional keyword arguments.
    Returns:
        None
    """

    if instance.pk:
        try:
            old_pic = Profile.objects.get(pk=instance.pk).pic
        except Profile.DoesNotExist:
            return
        else:
            if old_pic and old_pic != instance.pic:
                if os.path.isfile(old_pic.path):
                    os.remove(old_pic.path)