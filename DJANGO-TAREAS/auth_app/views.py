from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from auth_app.forms import *

# Create your views here.

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
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET": 
      return render(request, 'signin.html',{
        'form': CustomUserLoginForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None: #Si el usuario está vacío (incorrecto o inexistente) se muestra de nuevo el login con un error
             return render(request, 'signin.html',{
            'form': CustomUserLoginForm,
            'error': 'Las credenciales son incorrectas'
        })
        else: #Si las credenciales son correctas se arranca la sesión y se redirecciona a la vista tasks
            login(request, user)
            return redirect('tasks')