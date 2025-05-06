from django.contrib import admin
from django.urls import path, include  # <--- aggiunto include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),  # <--- collega gli URL della tua app
]
