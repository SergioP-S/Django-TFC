from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import List, Item
from django.db.models import Q
from .forms import *

# Create your views here.
@login_required
def lists(request):
    lists = List.objects.filter(Q(creator=request.user) | Q(collaborators=request.user)).order_by('created_on')

    return render(request, 'lists.html',{
        'title': 'Lists',
        'lists': lists
    })

@login_required
def list_details(request, list_id):
    #list_details = get_object_or_404(List, pk=list_id, user=request.user)
    list = get_object_or_404(List.objects.filter(Q(creator=request.user) | Q(collaborators=request.user)).distinct(),pk=list_id)
    items = Item.objects.filter(list=list_id).order_by('added_on')
    return render(request, 'list_details.html',{
        'title': "Detalles de la lista",
        'list': list,
        'items': items
    })

@login_required
def create_list(request): 
    if request.method == 'GET': 
        return render(request, 'create_list.html', {
            'form': ListForm
        })
    else:
        try:
            form = ListForm(request.POST)
            new_list = form.save(commit=False)
            new_list.creator = request.user
            new_list.save()
            return redirect('lists')
        except:
            return render(request, 'create_list.html', {
            'form': ListForm,
            'error': 'Error, introduzca datos válidos'
        })

@login_required
def add_item(request, list_id):
    #Se obtiene la lista a la que pertenece el item
    list_obj = get_object_or_404(List, pk=list_id)

    if request.method == 'GET': 
        print(f'list id es {list_id}')
        return render(request, 'add_item.html', {
            'form': NewItemForm,
            'list_id': list_id
        })
    else:
        try:
            form = NewItemForm(request.POST)
            new_item = form.save(commit=False)
            new_item.added_by = request.user
            new_item.list = list_obj
            new_item.save()
            print('Registro insertado')
            return redirect('lists')
        
        except:
            return render(request, 'add_item.html', {
            'form': ListForm,
            'error': 'Error, introduzca datos válidos'
        })

@login_required
def delete_item(request, item_id, list_id):
    item = get_object_or_404(Item, pk=item_id, added_by = request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('list_details', list_id=list_id)
    
