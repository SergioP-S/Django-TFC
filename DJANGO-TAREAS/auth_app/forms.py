from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .models import CustomUser
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput())