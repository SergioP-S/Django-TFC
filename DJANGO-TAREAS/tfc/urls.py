"""
URL configuration for tfc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views as tasksViews
from auth_app import views as auth_appViews
from lists import views as listsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tasksViews.home, name='home'),
    path('signup/',  auth_appViews.signup, name='signup'),
    path('signin/',  auth_appViews.signin, name='signin'),
    path('tasks/', tasksViews.tasks, name='tasks'),
    path('tasks_completed/', tasksViews.tasks_completed, name='tasks_completed'),
    path('logout/', auth_appViews.signout, name='logout'),
    path('tasks/create/', tasksViews.create_task, name='create'),
    path('tasks/<int:task_id>/', tasksViews.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', tasksViews.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', tasksViews.delete_task, name='delete_task'),
    path('lists/', listsViews.lists, name='lists'),
    path('lists/create/', listsViews.create_list, name='create_list'),
    path('lists/<int:list_id>/', listsViews.list_details, name='list_details'),
    path('lists/<int:list_id>/add_item/', listsViews.add_item, name='add_item'),
    path('lists/<int:list_id>/delete_item/<int:item_id>', listsViews.delete_item, name='delete_item')
    

]
