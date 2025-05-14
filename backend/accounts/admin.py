from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'has_seen_guide', 'dark_mode')
    search_fields = ('user__username', 'email')
