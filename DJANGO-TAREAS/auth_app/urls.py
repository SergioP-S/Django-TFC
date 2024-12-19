from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('user_details/<str:username>', views.user_details, name='user_details'),
    path('user_details/<str:username>/load_user_lists/', views.load_user_lists, name='load_user_lists'),
    path('verify_mail/', views.verify_mail, name='verify_mail'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('load_lists/', views.load_lists, name='load_lists'),
]