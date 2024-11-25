
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('completed/', views.tasks_completed, name='tasks_completed'),
    path('create/', views.create_task, name='create'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('<int:task_id>/delete/', views.delete_task, name='delete_task'),
]