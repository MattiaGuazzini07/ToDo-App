from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # ── autenticazione ─────────────────────────────────────────────
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="accounts/logout.html"
        ),
        name="logout",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/registration/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "registration/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/registration/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # ── app urls ───────────────────────────────────────────────────
    path("accounts/", include("backend.accounts.urls")),
    path("", include("backend.tasks.urls")),          # homepage = tasks:home
]

# media in debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
