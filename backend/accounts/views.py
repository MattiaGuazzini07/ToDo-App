from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm, UserSettingsForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models import Count, Q

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "🎉 Benvenuto su ToDo!")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.userprofile
    avatar_list = ['avatar0.png', 'avatar1.png', 'avatar2.png']  # etc.

    if request.method == 'POST':
        if 'toggle_dnd' in request.POST:
            profile.do_not_disturb = not profile.do_not_disturb
            profile.save()
            return redirect("profile")

        new_username = request.POST.get("username")
        if new_username and new_username != request.user.username:
            request.user.username = new_username
            request.user.save()
            return redirect("profile")

        avatar = request.POST.get('avatar')
        if avatar in avatar_list:
            profile.avatar = avatar
            profile.save()
            messages.success(request, "Avatar aggiornato!")
            return redirect("profile")

    return render(request, 'accounts/profile.html', {'avatar_list': avatar_list})

@login_required
def settings_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserSettingsForm(instance=profile)

    return render(request, 'accounts/settings.html', {'form': form})
