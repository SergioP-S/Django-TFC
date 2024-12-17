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
    limit = int(request.GET.get('limit', 10))
    public_lists = List.objects.filter(is_public=True)[offset:offset+limit]
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
    has_more = List.objects.filter(is_public=True).count() > offset + limit
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
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm,
    })
    else: 
        if request.POST['password1'] ==  request.POST['password2']:
           try: 
                validate_password(request.POST['password1'])
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'], is_active=False)
                user.save()
                # Create a profile for the new user
                profile = Profile(user=user, description='', pic='profile_pics/default.jpg')
                profile.save()
                # Generate verification key and expiration date
                verification_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
                expiration_date = datetime.now() + timedelta(days=1)
                request.session['verification_key'] = verification_key
                request.session['expiration_date'] = expiration_date.isoformat()
                request.session['user_id'] = user.id
                verification_link = request.build_absolute_uri(f"/verify_mail/?key={verification_key}")
                send_mail(
                    'Verify your email',
                    f'Click the link to verify your email: {verification_link}',
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
    key = request.GET.get('key')
    if key and key == request.session.get('verification_key'):
        expiration_date = datetime.fromisoformat(request.session.get('expiration_date'))
        if datetime.now() < expiration_date:
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'verify_mail.html', {'error': 'Verification link has expired'})
    return render(request, 'verify_mail.html', {'error': 'Invalid verification link'})


@login_required
def user_details(request, username): 
    user = get_object_or_404(User, username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist")
    lists = List.objects.filter(creator=user, is_public=True)
    print(lists)
    if request.method == 'GET': 
        return render(request, 'user_details.html', {
            'user_info': user,
            'profile': profile,
            'lists': lists
        })
    
def profile_settings(request):
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
            return redirect('home')
        else:
            return render(request, 'profile_settings.html', {
                'form': form,
                'error': 'Error al completar el formulario'
            })

@login_required
def delete_user(request):
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
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'reset_password.html', {'form': SetPasswordForm(user=request.user)})
        else:
            return render(request, 'reset_password_email.html', {'form': PasswordResetEmailForm()})
    else:
        if request.user.is_authenticated:
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                request.user.set_password(new_password)
                request.user.save()
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
                    'Password Reset',
                    f'Click the link to reset your password: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'reset_password_email.html', {'form': form, 'message': 'Email sent'})
            else:
                return render(request, 'reset_password_email.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
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
                return redirect('signin')
            else:
                return render(request, 'reset_password_confirm.html', {'form': form})
        else:
            form = PasswordResetForm(user)
            return render(request, 'reset_password_confirm.html', {'form': form})
    else:
        return render(request, 'reset_password_confirm.html', {'error': 'Invalid link'})