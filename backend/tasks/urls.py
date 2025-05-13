from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('uncomplete/<int:task_id>/', views.uncomplete_task, name='uncomplete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
]
