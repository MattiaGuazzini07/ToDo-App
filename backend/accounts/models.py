from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_seen_guide = models.BooleanField(default=False)
    avatar = models.CharField(max_length=200, default='avatar0.png')
    bio = models.TextField(blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    do_not_disturb = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"Profilo di {self.user.username}"

    def is_online(self):
        if self.last_seen:
            return (now() - self.last_seen).seconds < 300
        return False

    class Meta:
        db_table = "todo_userprofile"