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
    path('', auth_appViews.home, name='home'),
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
    path('lists/<int:list_id>/delete_item/<int:item_id>/', listsViews.delete_item, name='delete_item'),
    path('update_items/', listsViews.update_items, name='update_multiple'),
    path('lists/<int:list_id>/empty_list/', listsViews.empty_list, name='empty_list'),
    path('lists/<int:list_id>/modify/', listsViews.modify_list, name='modify_list'),
    path('lists/<int:list_id>/modify_item/<int:item_id>/', listsViews.modify_item, name='modify_item'),
    path('lists/<int:list_id>/delete/', listsViews.delete_list, name='delete_list'),
    path('lists/<int:list_id>/kick/<str:collaborator>', listsViews.kick_collaborator, name='kick_collaborator'),
    path('lists/<int:list_id>/leave/', listsViews.leave_list, name='leave_list'),
    path('lists/<int:list_id>/share/', listsViews.share_list, name='share_list'),
    path('lists/<int:list_id>/share/<str:signed_key>/', listsViews.accept_invitation, name='accept_invitation'),
    path('lists/<int:list_id>/complete/', listsViews.complete_list, name='complete_list'),
    path('lists/<int:list_id>/add_tag/', listsViews.add_tag, name='add_tag'),
    path('lists/<int:list_id>/delete_tags/', listsViews.delete_tags, name='delete_tags'),
    
       

]
