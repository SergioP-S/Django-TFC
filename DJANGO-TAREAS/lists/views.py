from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import List, Item, User
from django.db.models import Q
from .forms import *
import json
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core import signing

@login_required
def lists(request):
    """
    View function to display lists for the logged-in user.
    This function retrieves lists from the database where the logged-in user is either the creator or a collaborator.
    The lists are ordered by their creation date and duplicates are removed.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
    Returns:
        HttpResponse: The rendered 'lists.html' template with the context containing the title and the lists.
    """

    lists = List.objects.filter(Q(creator=request.user) | Q(collaborators=request.user)).order_by('created_on').distinct()
    return render(request, 'lists.html',{
        'title': 'Lists',
        'lists': lists
    })

@login_required
def list_details(request, list_id):
    """
    Returns a list object to list_details.html, containing 

    :param request: gets info about the request, such as method used (get or post) or user info. 
    :param list_id: id of the list required.
    :return: returns list_details.html view with a list object and a array containing all items associated to the list.
    """

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
    """
    If method is GET it shows create_list.html view with ListForm to fill attributes.
    If method is POST it creates a new List with the attributes obtained in ListForm and redirects to lists view, in case of error, it returns an error.
  
    :param request: gets info about the request, such as method used (get or post) or user info. 
    :return: renders a view, depending of the method its accessed.
    """

    #If method is GET, it renders create_list.html with ListForm to fill new list attributes
    if request.method == 'GET': 
        return render(request, 'create_list.html', {
            'form': ListForm
        })
    else:
        #If method is POST, it will try to insert the new record into List table
        try:
            form = ListForm(request.POST)
            new_list = form.save(commit=False)
            new_list.creator = request.user
            new_list.save()
            return redirect('lists')
        except:
            #In case of error creating the list, it returns the create_list.html view with an error message
            return render(request, 'create_list.html', {
            'form': ListForm,
            'error': 'Error, introduzca datos válidos'
        })

@login_required
def add_item(request, list_id):
    """
    If method is GET it shows add_item.html view with NewItemForm to fill attributes of the new Item.
    If method is POST it creates a new Item with the attributes of NewItemForm. It adds the item to the list especified in list_id

    :param request: gets info about the request, such as method used (get or post) or user info. 
    :param list_id: list where the item will be added.
    """

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
    """
    If method is GET it returns 404 page.
    If method is POST it deletes the record with the specified id.
  
    :param request: gets info about the request, such as method used (get or post) or user info.
    :param item_id: item id that will be deleted. 
    :param list_id: id of the list that will be returned after deleting the item.
    :return: renders list_details.html view, showing the list that containted the item.
    """
    
    item = get_object_or_404(Item, pk=item_id, added_by = request.user) #Cambiar la propiedad, ya que si intenta borrarlo otra persona (admin) no funcionará
    if request.method == 'POST':
        item.delete()
        return redirect('list_details', list_id=list_id)
    else :
        return 404

@login_required    
@csrf_exempt
def update_items(request):
    """
    Gets Ajax request to update is_done field on items 
  
    :param request: gets info about the JSON request, obtaining the items that were updated
    :return: renders a view, depending of the method its accessed.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  #Obtains data from AJAX request

            #Gets all items from the JSON
            for item_id, is_done in data.items():
                try:
                    item = Item.objects.get(id=item_id)  #Search by the item id
                    item.is_done = is_done  #Updates the is_done status
                    item.save()  #Save changes
                except Item.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'Item con id {item_id} no encontrado'})
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def empty_list(request, list_id):
    """
    Empties a list, deletes all items from a list
  
    :param request: gets info about the request, such as method used (get or post) or user info.
    :param list_id: list that will be emptied
    """
    if request.method == 'GET':
        #change to 404 not Found
        raise Http404
    else:
        try:
            items = Item.objects.filter(list=list_id)
            list = get_object_or_404(List, pk=list_id)
            print("Emptying list")
            print(items)
            items.delete()
            return redirect('list_details', list_id=list_id) #Redirects back to the list
        except Exception:
            #Falta agregar el redirect si falla
            return render(request, 'list_details.html', {
                'title': 'Lists',
                'error': "error",
                'list' : list
            })

@login_required
def modify_list(request, list_id):
    """
    Allows user to modify the list info.  

    :param request: gets info about the request, such as method used (get or post) or user info.
    :param list_id:
    """
    list = get_object_or_404(List, pk=list_id)
    if request.user == list.creator or request.user in list.collaborators.all():
        if request.method == 'GET': 
            form = ModifyListForm(instance=list)
            return render(request, 'modify_list.html', {
                'form': form,
                'list': list
            })
        else:
            try:
                form = ModifyListForm(request.POST, instance=list)
                if form.is_valid():
                    modified_list = form.save(commit=False)  # No se guarda aún en la base de datos
                    modified_list.last_modified = timezone.now() # Actualiza last_modified
                    modified_list.modified_by = request.user  # Establece modified_by
                    modified_list.save()  # Guarda finalmente en la base de datos
                    return redirect(f'/lists/{list_id}/')
            except Exception as e:
                return render(request, 'modify_list.html', {
                'form': ModifyListForm,
                'list': list,
                'error': "Error al modificar la lista"
                })
    else:
        raise Http404


def user_in_list(list_id, User):
    """
    Checks if an user is collaborator or the creator of the list, returns true or false 

    :param list_id: pk of the list that is going to be checked
    :param User: user info where it gets the username
    :return: True if the user is collaborator or creator of the list, False if its not collaborator or the creator.
    """
    try:
        list = List.objects.get(id=list_id)  
        if list.creator == User.username:
            print("Es el creador de la lista")
            return True
        elif list.collaborators == User.username:
            print("Es colaborador de la lista")
            return True
        else:
            print("No es ni colaborador ni creador de la lista")
            return False
    except List.DoesNotExist as e:
        return e
    
@login_required
def modify_item(request, list_id, item_id):
    """
    Modifies the selected item

    :param request: gets info about the request, such as method used (get or post) or user info.
    :param list_id: pk of the list for redirect purposes
    :param item_id: item that will be modified
    """

    item = get_object_or_404(Item, pk=item_id)
    list = get_object_or_404(List, pk=list_id)

    if request.user == list.creator or request.user in list.collaborators.all() or request.user == item.added_by:
        if request.method == 'GET': 
            form = ModifyItemForm(instance=item)
            return render(request, 'modify_item.html', {
                'form': form,
                'list': list, 
                'item': item
            })
        else:
            try:            
                form = ModifyItemForm(request.POST, instance=item)
                if form.is_valid():
                    modified_item = form.save(commit=False)  
                    modified_item.last_modified = timezone.now()
                    modified_item.modified_by = request.user  
                    modified_item.save()  
                    return redirect(f'/lists/{list_id}/')
                else:
                    return render(request, 'modify_item.html', {
                    'form': form,
                    'list': list, 
                    'item': item,
                    'error': "Error while modifying the item"
                    })
            except Exception as e:
                return HttpResponse(f"Error modifiying the list: {str(e)}", status=500)
                # return render(request, 'modify_list.html', {
                # 'form': ModifyItemForm,
                # 'error': "Error al modificar la lista"
                # })  
    else:
        raise Http404

@login_required
def delete_list(request, list_id):
    """
    Delete a specific list if the request method is POST and the user is the creator of the list.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        list_id (int): The ID of the list to be deleted.
    Returns:
        HttpResponseRedirect: Redirects to the 'lists' view if the list is successfully deleted.
    Raises:
        Http404: If the request method is not POST or the user is not the creator of the list.
    """

    list = get_object_or_404(List, pk=list_id)

    if request.method == 'POST' and request.user == list.creator: 
        list.delete()
        return redirect('lists')
    else:
        raise Http404
    




def accept_invitation(request, list_id, signed_key):
    """
    Handles the acceptance of an invitation to collaborate on a list.
    This function decodes the signed key to verify the invitation and checks if it has expired.
    If the invitation is valid and not expired, it adds the requesting user as a collaborator
    to the specified list.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to which the user is being invited.
        signed_key (str): The signed key containing the invitation details.
    Returns:
        HttpResponse: Redirects to the list details page if the invitation is accepted.
                        Renders an expired invitation page if the invitation has expired.
                        Returns a bad request response if the signature is invalid or expired.
    Raises:
        signing.SignatureExpired: If the signed key has expired.
        signing.BadSignature: If the signed key is invalid.
    """
    try:
        # Decoding the signature
        data = signing.loads(signed_key)
        expires_at = data['expires_at']

        # Verify if the invitation is expired
        if timezone.now().timestamp() > expires_at:
            return render(request, 'invitations/expired.html')  # CAMBIAR

        # Store invitation details in session if user is not authenticated
        if not request.user.is_authenticated:
            request.session['invitation'] = {'list_id': list_id, 'signed_key': signed_key}
            return redirect('signin')

        # Get the list and add the user as a collaborator
        list = get_object_or_404(List, id=list_id)
        list.collaborators.add(request.user)  # Assuming you have a many-to-many relationship
        list.save()

        return redirect('list_details', list_id=list.id)

    except signing.SignatureExpired:
        return HttpResponseBadRequest("La invitación ha expirado.")
    except signing.BadSignature:
        return HttpResponseBadRequest("Invitación no válida.")

@login_required
def share_list(request, list_id):
    """
    Share a list by generating a signed URL with an expiration date.
    This view handles the sharing of a list by creating a signed URL that includes
    the list ID and an expiration timestamp. The URL is valid for one week from the
    time of creation. The signed URL can be used to accept an invitation to access
    the list.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to be shared.
    Returns:
        HttpResponse: If the request method is GET, renders the 'share_list.html' template
                      with the list and the generated share URL.
    """

    list = get_object_or_404(List, pk=list_id)

    # Establecer la fecha de caducidad (1 semana desde el momento actual)
    expires_at = timezone.now() + timezone.timedelta(weeks=1)
    expiration_timestamp = int(expires_at.timestamp())  # Pasamos la fecha de expiración a timestamp

    # Crear una clave firmada que incluye el ID de la lista y la fecha de caducidad
    data = {'list_id': list_id, 'expires_at': expiration_timestamp}
    signed_key = signing.dumps(data)

    # Generar la URL completa con la clave firmada
    share_url = request.build_absolute_uri(reverse('accept_invitation', args=[list_id,signed_key]))

    if request.method == 'GET':
        return render(request, 'share_list.html', {
            'list': list,
            'share_url': share_url
        })

@login_required
def kick_collaborator(request, collaborator, list_id):
    """
    Remove a collaborator from a list.
    Args:
        request (HttpRequest): The HTTP request object.
        collaborator (str): The username of the collaborator to be removed.
        list_id (int): The ID of the list from which the collaborator will be removed.
    Raises:
        Http404: If the request method is GET or if the list or collaborator does not exist.
    Returns:
        HttpResponse: Renders the 'list_details.html' template with the updated list.
    """

    list = get_object_or_404(List, pk=list_id)
    collaborator = get_object_or_404(User, username = collaborator)

    if request.method == 'GET':
        raise Http404
    else:
        if collaborator in list.collaborators.all():
            list.collaborators.remove(collaborator)
            list.save()
            return render(request, 'list_details.html', {
                'title': 'Lists',
                'list' : list
            })
        else:
            return render(request, 'list_details.html', {
                'title': 'Lists',
                'error': "error",
                'list' : list
            })


