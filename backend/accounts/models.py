from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

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

class Friendship(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendships_sent',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendships_received',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("You can't send a friend request to yourself.")

    def __str__(self):
        status = "Accepted" if self.accepted else "Pending"
        return f"{self.from_user} ➝ {self.to_user} ({status})"
