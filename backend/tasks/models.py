from django.db import models
from django.contrib.auth.models import User
from backend.accounts.models import Team


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Bassa'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed_at = models.DateTimeField(null=True, blank=True)
    team = models.ForeignKey('accounts.Team', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "todo_task"

class TeamTask(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Bassa'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]

    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    teams = models.ManyToManyField(Team, related_name='team_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
