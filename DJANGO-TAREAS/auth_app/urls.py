
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('user_details/<str:username>', views.user_details, name='user_details'),
    path('complete_profile/', views.complete_profile, name="complete_profile"),
]