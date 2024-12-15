from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('user_details/<str:username>', views.user_details, name='user_details'),
    path('complete_profile/', views.complete_profile, name="complete_profile"),
    path('verify_mail/', views.verify_mail, name='verify_mail'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
]