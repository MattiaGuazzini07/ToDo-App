from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return f"Profilo di {self.user.username}"

# Crea profilo automaticamente dopo la registrazione
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()