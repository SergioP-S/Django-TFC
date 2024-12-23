from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
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
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Descripción', 'class': 'w-full p-2 border rounded', 'rows': 4})
    )
    class Meta:
        model = Profile
        fields = ['description']

class PasswordResetForm(SetPasswordForm):
    pass

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField()