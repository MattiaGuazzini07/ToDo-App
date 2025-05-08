from django.urls import path
from . import views
from .views import admin_dashboard, user_tasks

urlpatterns = [
    path('', views.home, name='home'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('uncomplete/<int:task_id>/', views.uncomplete_task, name='uncomplete_task'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/user/<int:user_id>/', user_tasks, name='user_tasks'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('create_user/', views.create_user, name='create_user'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
]
