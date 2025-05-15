from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("signup/", views.signup, name="signup"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/user/<int:user_id>/", views.user_tasks, name="user_tasks"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    path('users/', views.user_list, name='user_list'),
    path('users/<str:username>/', views.user_profile, name='user_profile'),
    path('users/<str:username>/add/', views.send_friend_request, name='send_friend_request'),
    path('users/<str:username>/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('autocomplete/user/', views.user_autocomplete, name='user_autocomplete'),
    path('team/<int:pk>/delete/', views.delete_team, name='delete_team'),
]
