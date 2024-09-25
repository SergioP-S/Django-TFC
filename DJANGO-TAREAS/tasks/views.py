from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request): 
    return render(request, 'home.html')


@login_required
def tasks(request):
    #tasks = Task.objects.filter(user= request.user, date_completed__isnull = True) #Las tareas que se muestran serán las del usuario que ha iniciado sesión y que no se hayan completado

    sort_mode = request.GET.get('sort_mode')  # Obtener el parámetro sort_mode de la URL
    
    if sort_mode == '1':
        # Ordenar por el campo date_completed, el más antiguo primero
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=True).order_by('date_completed')
    elif sort_mode == '2':
        # Ordenar por el campo important (mostrar primero los True)
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=True).order_by('-important', '-created_at')
    elif sort_mode == '3':
        # Ordenar por el campo title, en orden alfabético
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=True).order_by('title')
    else:
        # Ordenar por el campo date_completed (por defecto), más reciente primero
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=True).order_by('-date_completed')

    return render(request, 'tasks.html', {
        'title': "Tareas Pendientes",
        'tasks': tasks,
        'date_field': "Fecha de Creación",
        'url_name': "tasks"
    })

# @login_required
# def tasks_completed(request):
#     tasks = Task.objects.filter(user= request.user, date_completed__isnull = False).order_by('-date_completed') #Las tareas que se muestran serán las del usuario que ha iniciado sesión y que no se hayan completado
#     return render(request, 'tasks.html', {
#         'title': "Tareas Completadas",
#         'tasks': tasks
#     })

@login_required
def tasks_completed(request):
    sort_mode = request.GET.get('sort_mode')  # Obtener el parámetro sort_mode de la URL
    if sort_mode == '1':
        # Ordenar por el campo date_completed, el más antiguo primero
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('date_completed')
    elif sort_mode == '2':
        # Ordenar por el campo important (mostrar primero los True)
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-important', '-date_completed')
    elif sort_mode == '3':
        # Ordenar por el campo title, en orden alfabético
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('title')
    else:
        # Ordenar por el campo date_completed (por defecto), más reciente primero
        tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')

    return render(request, 'tasks.html', {
        'title': "Tareas Completadas",
        'tasks': tasks, 
        'date_field': "Completada el",
        'url_name': "tasks_completed"
    })


#@login_required
# def signout(request):
#     logout(request)
#     return redirect('home')

# def signin(request):
#     if request.method == "GET": 
#       return render(request, 'signin.html',{
#         'form': AuthenticationForm
#     })
#     else:
#         user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#         if user is None: #Si el usuario está vacío (incorrecto o inexistente) se muestra de nuevo el login con un error
#              return render(request, 'signin.html',{
#             'form': AuthenticationForm,
#             'error': 'Las credenciales son incorrectas'
#         })
#         else: #Si las credenciales son correctas se arranca la sesión y se redirecciona a la vista tasks
#             login(request, user)
#             return redirect('tasks')
        
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Error, introduzca datos válidos'
        })

@login_required
def task_detail(request, task_id):
   if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task' : task,
            'form' : form
        })
   else: 
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task' : task,
            'form' : form,
            'error' : "Error al actualizar la tarea"
        })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user) #Se obtiene la tarea con el id solicitado y si es propietario del usuario de la sesión.
    if request.method == 'POST': #Si se llama al metodo POST, significa que ha enviado el formulario de completar tarea
        task.date_completed = timezone.now() #Se marca la tarea como completada introduciendo la fecha y hora actual
        task.save() #La tarea se guarda y se actualiza el registro de la Base de datos
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')