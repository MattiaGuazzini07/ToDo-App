from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Team

class UserForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Questo username è già in uso.")
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        return user

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'dark_mode']
        labels = {
            'email': 'Email alternativa',
            'dark_mode': 'Tema scuro',
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome del team'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrizione'}),
        }

class InviteMemberForm(forms.Form):
    username = forms.CharField(
        label='Username da invitare',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es. giulia123'})
    )
    role = forms.ChoiceField(
        choices=[('member', 'Member'), ('admin', 'Admin')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )