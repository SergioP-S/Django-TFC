import base64
import random
import string
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from auth_app.forms import *
from lists.models import List
from auth_app.models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
import uuid
from django.utils import timezone


def home(request): 
    """
    Renders the home page.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, 'home.html')


def load_lists(request):
    """
    Handles AJAX requests to load lists in batches.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the lists and a flag indicating if there are more lists to load.
    """
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 30))
    search_query = request.GET.get('search', '')
    public_lists = List.objects.filter(is_public=True, name__icontains=search_query).order_by('-created_on')[offset:offset+limit]
    lists_data = [{
        'id': list.id,
        'name': list.name,
        'creator': {
            'username': list.creator.username,
            'profile': {
                'pic': list.creator.profile.pic.url if list.creator.profile.pic else 'profile_pics/default.jpg'
            }
        }
    } for list in public_lists]
    has_more = List.objects.filter(is_public=True, name__icontains=search_query).count() > offset + limit
    return JsonResponse({'lists': lists_data, 'has_more': has_more})


def signup(request):

    """
    Handle user signup process.
    If the request method is GET, render the signup form.
    If the request method is POST, validate the form data and create a new user if the data is valid.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object. If the request method is GET, returns the signup form.
                    If the request method is POST and the form data is valid, redirects to the 'tasks' page.
                    If the form data is invalid, re-renders the signup form with error messages.
    """
 
    if request.method == 'GET': 
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm,
        })
    else: 
        if request.POST['password1'] ==  request.POST['password2']:
           try: 
                validate_password(request.POST['password1'])
                if User.objects.filter(username=request.POST['username']).exists():
                    raise IntegrityError('El usuario ya existe')
                if User.objects.filter(email=request.POST['email']).exists():
                    raise IntegrityError('El correo electrónico ya está en uso')
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'], is_active=False)
                user.save()
                # Create a profile for the new user
                profile = Profile(user=user, description='', pic='profile_pics/default.jpg')
                # Generate verification key and expiration date
                verification_key = str(uuid.uuid4())
                profile.verification_key = verification_key
                profile.verification_key_expiration = timezone.now() + timezone.timedelta(days=1)
                profile.save()
                verification_link = request.build_absolute_uri(f"/verify_mail/?key={verification_key}")
                send_mail(
                    'Verifique su correo electrónico, Listopia',
                    f'Por favor, acceda a este enlace para verificar su cuenta: {verification_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('verify_mail')
           except ValidationError as e:
                return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    "error": e.messages
                })
           except IntegrityError as e: 
                return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    "error": str(e)
                })
        return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    "error": 'Las contraseñas no coinciden'
                })
    
@login_required
def signout(request):
    """
    Handle user sign-out process.
    Logs out the user and redirects to the home page.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: A redirect to the home page.
    """
    logout(request)
    return redirect('home')

def signin(request):
    """
    Handle user sign-in process.
    If the request method is GET, render the sign-in form.
    If the request method is POST, authenticate the user with the provided credentials.
    If authentication fails, render the sign-in form with an error message.
    If the user is not active, redirect to the email verification page.
    If authentication is successful, log the user in and redirect to the appropriate page.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object with the rendered sign-in form or a redirect.
    """

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
        elif not user.is_active:
            return redirect('verify_mail')
        else:  # If the credentials are correct, start the session and redirect to the tasks view
            login(request, user)
            # Check for pending invitation in session
            invitation = request.session.pop('invitation', None)
            if invitation:
                return redirect('accept_invitation', list_id=invitation['list_id'], signed_key=invitation['signed_key'])
            return redirect('home')
        

def verify_mail(request):
    """
    View function to verify a user's email address.
    This function handles the verification of a user's email address by checking
    a verification key provided in the request. If the user is authenticated, it
    raises a 404 error. If the verification key matches the one stored in the session
    and has not expired, the user's account is activated, and they are logged in.
    Otherwise, an error message is displayed.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
    Returns:
        HttpResponse: A redirect to the home page if verification is successful.
                      A rendered 'verify_mail.html' template with an error message if verification fails.
    """

    key = request.GET.get('key')
    if not key:
        return render(request, 'verify_mail.html')

    try:
        profile = Profile.objects.get(verification_key=key)
    except Profile.DoesNotExist:
        return render(request, 'verify_mail.html', {'error': 'Enlace de verificación inválido'})

    if profile.verification_key_expiration and timezone.now() < profile.verification_key_expiration:
        user = profile.user
        user.is_active = True
        profile.verification_key = None
        profile.verification_key_expiration = None
        user.save()
        profile.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'verify_mail.html', {'error': 'El link de verificación ha expirado'})


@login_required
def user_details(request, username): 
    """
    Display user details and profile information.
    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose details are to be displayed.
    Returns:
        HttpResponse: The rendered user details page.
    """
    user = get_object_or_404(User, username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist")
    if request.method == 'GET': 
        return render(request, 'user_details.html', {
            'user_info': user,
            'profile': profile,
        })

@login_required
def load_user_lists(request, username):
    """
    Load public lists created by a specific user.
    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose lists are to be loaded.
    Returns:
        JsonResponse: A JSON response containing the lists and a flag indicating if there are more lists to load.
    """
    user = get_object_or_404(User, username=username)
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))
    lists = List.objects.filter(creator=user, is_public=True)[offset:offset+limit]
    lists_data = [{'id': list.id, 'name': list.name} for list in lists]
    has_more = List.objects.filter(creator=user, is_public=True).count() > offset + limit
    return JsonResponse({'lists': lists_data, 'has_more': has_more})

@login_required
def profile_settings(request):
    """
    Handle profile settings update.
    If the request method is GET, render the profile settings form.
    If the request method is POST, validate and save the form data.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered profile settings page with success or error messages.
    """
    if request.method == 'GET':
        if hasattr(request.user, 'profile'):
            profile = get_object_or_404(Profile, user=request.user)
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()
        return render(request, 'profile_settings.html', {
            'form': form,
        })
    else:
        if hasattr(request.user, 'profile'):
            profile = get_object_or_404(Profile, user=request.user)
            form = ProfileForm(request.POST, request.FILES, instance=profile)
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
            elif not profile.pic:
                profile.pic = 'profile_pics/default.jpg'
            profile.save()
            return render(request, 'profile_settings.html', {
                'form': form,
                'success': 'Perfil actualizado correctamente'
            })
        else:
            return render(request, 'profile_settings.html', {
                'form': form,
                'error': 'Error al completar el formulario'
            })

@login_required
def delete_user(request):
    """
    Handle user account deletion.
    If the request method is POST, validate the password and delete the user account if the password is correct.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: A redirect to the home page or the profile settings page with an error message.
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            request.user.delete()
            return redirect('home')
        else:
            return render(request, 'profile_settings.html', {
                'form': ProfileForm(instance=request.user.profile),
                'delete_error': 'Incorrect password'
            })
    return redirect('profile_settings')

def reset_password(request):
    """
    Handle password reset process.
    If the request method is GET, render the password reset form.
    If the request method is POST, validate the form data and reset the password if the data is valid.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered password reset page or a redirect to the sign-in page.
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'reset_password.html', {'form': PasswordResetForm(user=request.user)})
        else:
            return render(request, 'reset_password_email.html', {'form': PasswordResetEmailForm()})
    else:
        if request.user.is_authenticated:
            form = PasswordResetForm(user=request.user, data=request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                request.user.set_password(new_password)
                request.user.save()
                send_mail(
                    'Contraseña Reestablecida Correctamente',
                    'Su contraseña ha sido reestablecida.',
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
                return redirect('signin')
            else:
                return render(request, 'reset_password.html', {'form': form})
        else:
            form = PasswordResetEmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = get_object_or_404(User, email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f"/reset_password_confirm/{uid}/{token}/")
                send_mail(
                    'Reestablecimiento de contraseña para Listopia',
                    f'Entre en este enlace para reestablecer la contraseña de su cuenta: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'reset_password_email.html', {'form': form, 'message': 'Email sent'})
            else:
                return render(request, 'reset_password_email.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    """
    Handle password reset confirmation.
    Validate the token and reset the password if the token is valid.
    Args:
        request (HttpRequest): The HTTP request object.
        uidb64 (str): The base64 encoded user ID.
        token (str): The password reset token.
    Returns:
        HttpResponse: The rendered password reset confirmation page or a redirect to the sign-in page.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(user, request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                # Send email notification
                send_mail(
                    'Contraseña Reestablecida Correctamente',
                    'Su contraseña ha sido reestablecida.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('signin')
            else:
                return render(request, 'reset_password_confirm.html', {'form': form})
        else:
            form = PasswordResetForm(user)
            return render(request, 'reset_password_confirm.html', {'form': form})
    else:
        return render(request, 'reset_password_confirm.html', {'error': 'Invalid link'})