from django.urls import path
from . import views

urlpatterns = [
    path('', views.lists, name='lists'),
    path('create/', views.create_list, name='create_list'),
    path('<int:list_id>/', views.list_details, name='list_details'),
    path('<int:list_id>/add_item/', views.add_item, name='add_item'),
    path('<int:list_id>/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('<int:list_id>/empty_list/', views.empty_list, name='empty_list'),
    path('<int:list_id>/modify/', views.modify_list, name='modify_list'),
    path('<int:list_id>/modify_item/<int:item_id>/', views.modify_item, name='modify_item'),
    path('<int:list_id>/delete/', views.delete_list, name='delete_list'),
    path('<int:list_id>/kick/<str:collaborator>', views.kick_collaborator, name='kick_collaborator'),
    path('<int:list_id>/leave/', views.leave_list, name='leave_list'),
    path('<int:list_id>/share/', views.share_list, name='share_list'),
    path('<int:list_id>/share/<str:signed_key>/', views.accept_invitation, name='accept_invitation'),
    path('<int:list_id>/add_tag/', views.add_tag, name='add_tag'),
    path('<int:list_id>/delete_tags/', views.delete_tags, name='delete_tags'),
    path('<int:list_id>/get_details/', views.get_list_details, name='get_list_details'),
]