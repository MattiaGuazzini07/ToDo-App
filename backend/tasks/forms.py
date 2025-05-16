from django import forms
from .models import Task, TeamTask
from backend.accounts.models import Team

class TaskForm(forms.ModelForm):
    is_completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-switch',
            'id': 'isCompletedSwitch'
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'team', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'team': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['team'].queryset = Team.objects.filter(members__user=user)
        else:
            self.fields['team'].queryset = Team.objects.none()


class TeamTaskForm(forms.ModelForm):
    class Meta:
        model = TeamTask
        fields = ['title', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titolo attività di team'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)