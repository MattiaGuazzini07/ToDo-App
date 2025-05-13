from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Bassa'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]
    # Definizione del modello Task
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # last_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

# Modello per il profilo utente
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_seen_guide = models.BooleanField(default=False)
    avatar = models.CharField(max_length=200, default='default1.png')
    bio = models.TextField(blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profilo di {self.user.username}"

    def is_online(self):
        from django.utils.timezone import now
        if self.last_seen:
            return (now() - self.last_seen).seconds < 300  # 5 minuti
        return False

