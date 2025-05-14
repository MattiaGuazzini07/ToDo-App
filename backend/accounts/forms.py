from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

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
        fields = ['email', 'prefers_dark_mode']
        labels = {
            'email': 'Email alternativa',
            'prefers_dark_mode': 'Tema scuro',
        }
