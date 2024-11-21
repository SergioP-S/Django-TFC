from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .models import CustomUser
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput())

class ProfileForm(forms.ModelForm):
    class Meta():
            model = Profile
            fields = ['description']