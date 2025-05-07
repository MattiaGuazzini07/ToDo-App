from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'priority': forms.Select(),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Mostra la password come input nascosto
        }