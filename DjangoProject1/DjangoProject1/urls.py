from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todo import views

from django.conf import settings
from django.conf.urls.static import static  # 👈 serve per servire i media file in debug

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='todo/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('', include('todo.urls')),
]

#Serve I file media solo se DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
