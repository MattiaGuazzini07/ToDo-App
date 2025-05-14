from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("signup/", views.signup, name="signup"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),  # ✅ qui
    path("admin-dashboard/user/<int:user_id>/", views.user_tasks, name="user_tasks"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
]
