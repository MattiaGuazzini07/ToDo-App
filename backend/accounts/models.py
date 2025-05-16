from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from typing import Any, Optional

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

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')

    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Member', 'Member'),
    ]
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)  # ← se non esiste, aggiungilo qui

    class Meta:
        unique_together = ('team', 'user')

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)  # ✅ CORRETTO
        self.completed_tasks_count = None

    def __str__(self):
        return f"{self.user.username} in {self.team.name} as {self.role}"
