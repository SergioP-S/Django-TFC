from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
#from .models import CustomUser
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'w-full p-2 border rounded'}),
        }
        help_texts = {
            'username': '',
            'password1': '',  # Limpia los textos de ayuda
            'password2': '',
        }

    # Sobrescribe los campos para personalizar los estilos
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'w-full p-2 border rounded'
        }),
        help_text='<small class="text-gray-600">Tu nombre de usuario no se podrá cambiar, ¡Piensatelo!</small>'
    )

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'w-full p-2 border rounded mb-3'
        })
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'w-full p-2 border rounded'
        }),
        help_text='<small class="text-gray-600">Debe contener al menos 8 caracteres y no ser completamente numérica.</small>'
    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña',
            'class': 'w-full p-2 border rounded'
        }),
        help_text='<small class="text-gray-600">Ambas contraseñas deben coincidir.</small>'
    )
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'w-full p-2 border rounded mb-3'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'w-full p-2 border rounded mb-3'}))

class ProfileForm(forms.ModelForm):
    description = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Escribe algo sobre tí...', 'class': 'w-full p-2 border rounded', 'rows': 4})
    )
    class Meta:
        model = Profile
        fields = ['description']

class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nueva contraseña',
            'class': 'w-full p-2 border rounded',
            'autocomplete': 'new-password'
        }),
        help_text='<small class="text-gray-600">Debe contener al menos 8 caracteres y no ser completamente numérica.</small>'
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar nueva contraseña',
            'class': 'w-full p-2 border rounded',
            'autocomplete': 'new-password'
        }),
        help_text='<small class="text-gray-600">Ambas contraseñas deben coincidir.</small>'
    )

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'w-full p-2 border rounded mb-3'
        }),
        help_text='<small class="text-gray-600">Introduce el correo electrónico asociado a tu cuenta. Se enviará un enlace para reestablecer su contraseña.</small>'
    )