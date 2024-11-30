import base64
import os
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from auth_app.forms import *

# Create your views here.


def home(request): 
    return render(request, 'home.html')



def signup(request):
 
    if request.method == 'GET': 
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm,
    })
    
    else: 
        if request.POST['password1'] ==  request.POST['password2']: #se cotejan las contraseñas
           try: 
                # Registro de usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.save()
                login(request, user) #arranca la cookie de sesión 
                #return HttpResponse('Usuario creado con éxito')
                return redirect('tasks')
           except IntegrityError: 
                return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    "error": 'Las contraseñas no coinciden'
                })
    
@login_required
def signout(request):
    """
    Logs out the current user and redirects to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the home page.
    """
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET": 
        return render(request, 'signin.html', {
            'form': CustomUserLoginForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:  # If the user is incorrect or does not exist, show the login form with an error
            return render(request, 'signin.html', {
                'form': CustomUserLoginForm,
                'error': 'Las credenciales son incorrectas'
            })
        else:  # If the credentials are correct, start the session and redirect to the tasks view
            login(request, user)
            # Check for pending invitation in session
            invitation = request.session.pop('invitation', None)
            if invitation:
                return redirect('accept_invitation', list_id=invitation['list_id'], signed_key=invitation['signed_key'])
            return redirect('home')
        


def user_details(request, username): 
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user = request.user.id)
    if request.method == 'GET': 
        return render(request, 'user_details.html', {
            'user_info': user,
            'profile' : profile
        })
    

def complete_profile(request): 
    if request.method == 'GET':
        return render(request, 'complete_profile.html', {
            'form': ProfileForm,
        })
    else:
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            cropped_image_data = request.POST.get('cropped_image_data')
            if cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{request.user.id}.{ext}')
                profile.pic = data

            profile.save()
            return redirect('home')
        else:
            return render(request, 'complete_profile.html', {
                'form': ProfileForm,
                'error': 'Error al completar el formulario'
            })