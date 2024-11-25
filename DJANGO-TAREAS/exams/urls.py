from django.urls import path
from . import views

urlpatterns = [
    path('share_exam/', views.share_exam, name='share_exam'),
    path('manage_permits/', views.manage_permits, name='manage_permits'),
    path('<int:exam_id>/', views.exam_details, name='exam_details'),
    path('', views.exams, name='exams'),
    path('<int:exam_id>/new_question/', views.add_question, name='add_question'),
    path('create_exam/', views.create_exam, name='create_exam'),
]