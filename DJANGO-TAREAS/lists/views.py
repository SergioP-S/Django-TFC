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
import qrcode # type: ignore
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

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
    View function to display the details of a specific list.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to be displayed.
    Returns:
        HttpResponse: The rendered HTML page displaying the list details.
    Raises:
        Http404: If the list with the given ID does not exist or the user does not have permission to view it.
    """
    

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
    Handles the creation of a new list.
    If the request method is GET, it renders the create_list.html template with an empty ListForm.
    If the request method is POST, it attempts to create a new list with the provided data.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered create_list.html template with the form or error message if the method is GET or if there is an error.
        HttpResponseRedirect: Redirects to the 'lists' view if the list is successfully created.
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
    Handles the addition of a new item to a specific list.
    Args:
    request (HttpRequest): The HTTP request object containing metadata about the request.
    list_id (int): The ID of the list to which the item will be added.
    Returns:
    HttpResponse: Renders the 'add_item.html' template with a form if the request method is GET.
    HttpResponseRedirect: Redirects to the 'lists' view if the item is successfully added.
    HttpResponse: Renders the 'add_item.html' template with an error message if there is an exception.
    Raises:
    Http404: If the list with the given list_id does not exist.
    """


    list_obj = get_object_or_404(List, pk=list_id)

    if request.method == 'GET': 
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
            items = Item.objects.filter(list=list_obj).order_by('added_on')
            return redirect('list_details', list_id=list_id)
        except:
            return render(request, 'add_item.html', {
            'form': ListForm,
            'error': 'Error, introduzca datos válidos'
            })

@login_required
def delete_item(request, item_id, list_id):
    """
    Deletes an item from a list if the request method is POST and the item was added by the current user.
    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to be deleted.
        list_id (int): The ID of the list containing the item.
    Returns:
        HttpResponseRedirect: Redirects to the list details page if the item is successfully deleted.
        HttpResponse: Returns a 404 response if the request method is not POST or the item does not exist.
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
    Handle the update of items' status via an AJAX POST request.
    This view function processes a POST request containing JSON data with item IDs and their corresponding 
    'is_done' status. It updates the status of each item in the database.
    Args:
        request (HttpRequest): The HTTP request object containing the POST data.
    Returns:
        JsonResponse: A JSON response indicating the success or failure of the update operation.
            - {'success': True} if all items were successfully updated.
            - {'success': False, 'error': 'Item con id {item_id} no encontrado'} if an item with the given ID does not exist.
            - {'success': False, 'error': 'Datos inválidos'} if the JSON data is invalid.
            - {'success': False, 'error': 'Método no permitido'} if the request method is not POST.
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
    Empties the items in a specified list.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to be emptied.
    Raises:
        Http404: If the request method is GET.
    Returns:
        HttpResponse: Redirects to the list details page if successful.
        HttpResponse: Renders the list details page with an error message if an exception occurs.
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
    View to modify an existing list.
    This view allows the creator of the list or any of its collaborators to modify the list.
    If the request method is GET, it renders a form pre-filled with the list's current data.
    If the request method is POST, it attempts to save the modified list data.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to be modified.
    Returns:
        HttpResponse: If the request method is GET, renders the 'modify_list.html' template with the form and list data.
                      If the request method is POST and the form is valid, redirects to the list's detail page.
                      If the request method is POST and the form is invalid, renders the 'modify_list.html' template with an error message.
    Raises:
        Http404: If the user is neither the creator nor a collaborator of the list.
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


def user_in_list(list_id, user):
    """
    Check if a user is either the creator or a collaborator of a list.
    Args:
        list_id (int): The ID of the list to check.
        user (User): The user to check against the list.
    Returns:
        bool: True if the user is the creator or a collaborator of the list, False otherwise.
    Raises:
        List.DoesNotExist: If the list with the given ID does not exist.
    """
    
    try:
        list = List.objects.get(id=list_id)  
        if list.creator == user:
            print("Es el creador de la lista")
            return True
        elif user in list.collaborators.all():
            print("Es colaborador de la lista")
            return True
        else:
            print("No es ni colaborador ni creador de la lista")
            return False
    except List.DoesNotExist:
        return False
    
@login_required
def modify_item(request, list_id, item_id):
    """
    Modify an item in a list.
    This view handles the modification of an item in a specific list. It checks if the user has the necessary permissions
    to modify the item and processes the form submission for modifying the item.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list containing the item.
        item_id (int): The ID of the item to be modified.
    Returns:
        HttpResponse: Renders the 'modify_item.html' template with the form for GET requests.
                      Redirects to the list view upon successful modification for POST requests.
                      Returns an error message if the modification fails.
                      Raises Http404 if the user does not have permission to modify the item.
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


def generate_share_url(list_id):
    """
    Generate a signed URL for sharing a list.
    Args:
        list_id (int): The ID of the list to be shared.
    Returns:
        str: The generated share URL.
    """
    expires_at = timezone.now() + timezone.timedelta(weeks=1)
    expiration_timestamp = int(expires_at.timestamp())
    data = {'list_id': list_id, 'expires_at': expiration_timestamp}
    signed_key = signing.dumps(data)
    share_url = reverse('accept_invitation', args=[list_id, signed_key])
    return share_url


def generate_qr_code(url):
    """
    Generate a QR code for the given URL.
    Args:
        url (str): The URL to be encoded in the QR code.
    Returns:
        str: The base64 encoded string of the generated QR code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

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

    list_obj = get_object_or_404(List, pk=list_id)
    share_url = request.build_absolute_uri(generate_share_url(list_id))
    qr_code_base64 = generate_qr_code(share_url)

    if request.method == 'GET':
        return render(request, 'share_list.html', {
            'list': list_obj,
            'share_url': share_url,
            'qr_code_base64': qr_code_base64
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


@login_required
def leave_list(request, list_id):
    """
    Allows a collaborator to leave a list.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to leave.
    Raises:
        Http404: If the request method is GET or if the list does not exist.
    Returns:
        HttpResponseRedirect: Redirects to the 'lists' view if the user successfully leaves the list.
    """
    list = get_object_or_404(List, pk=list_id)

    if request.method == 'GET':
        raise Http404
    else:
        if request.user in list.collaborators.all():
            list.collaborators.remove(request.user)
            list.save()
            return redirect('lists')
        else:
            return HttpResponseBadRequest("No eres colaborador de esta lista.")

@login_required
def complete_list(request, list_id):
    """
    Mark all items in a list as completed.
    Args:
        request (HttpRequest): The HTTP request object.
        list_id (int): The ID of the list to be completed.
    Returns:
        HttpResponseRedirect: Redirects to the list details page after marking all items as completed.
    """
    list_obj = get_object_or_404(List, pk=list_id)
    items = Item.objects.filter(list=list_obj)
    items.update(is_done=True)
    return redirect('list_details', list_id=list_id)