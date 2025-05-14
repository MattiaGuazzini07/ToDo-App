import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .forms import UserForm, UserSettingsForm
from .models import UserProfile
from backend.tasks.models import Task
from backend.tasks.forms import TaskForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "🎉 Benvenuto su ToDo!")
            return redirect('tasks:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    profile = request.user.userprofile

    avatar_dir = os.path.join(settings.STATICFILES_DIRS[0], "img", "avatars")
    avatar_list = sorted([
        f for f in os.listdir(avatar_dir)
        if f.endswith(".png")
    ])

    if request.method == 'POST':
        if 'toggle_dnd' in request.POST:
            profile.do_not_disturb = not profile.do_not_disturb
            profile.save()
            return redirect('accounts:profile')

        new_username = request.POST.get("username")
        if new_username and new_username != request.user.username:
            request.user.username = new_username
            request.user.save()
            return redirect('accounts:profile')

        avatar = request.POST.get('avatar')
        if avatar in avatar_list:
            profile.avatar = avatar
            profile.save()
            messages.success(request, "Avatar aggiornato!")
            return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'avatar_list': avatar_list})


@login_required
def settings_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserSettingsForm(instance=profile)

    return render(request, 'accounts/settings.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort_by", "username")

    allowed_sort_fields = ['username', '-username', 'email', '-email', 'date_joined', '-date_joined']
    if sort_by not in allowed_sort_fields:
        sort_by = 'username'

    form = UserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, f"Utente '{form.cleaned_data['username']}' creato con successo ✅")
            return redirect('accounts:admin_dashboard')
        except IntegrityError:
            form.add_error('username', 'Questo username è già in uso.')
            messages.error(request, "Username già in uso.")

    pinned_email = "mattiaguazzini007@gmail.com"
    pinned_user = User.objects.filter(email=pinned_email).annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__is_completed=True))
    ).first()

    users = User.objects.annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__is_completed=True))
    ).exclude(email=pinned_email).order_by(sort_by)

    return render(request, 'tasks/admin/admin_dashboard.html', {
        'form': form,
        'pinned_user': pinned_user,
        'users': users,
        'query': query,
        'sort_by': sort_by,
        'total_users': User.objects.count(),
    })


@user_passes_test(lambda u: u.is_superuser)
def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    completed_count = tasks.filter(is_completed=True).count()
    total_count = tasks.count()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.is_completed = False
            task.completed_at = None
            task.save()
            messages.success(request, "Task creato con successo ✅")
            return redirect('accounts:user_tasks', user_id=user.id)
    else:
        form = TaskForm()

    return render(request, 'tasks/admin/user_tasks.html', {
        'user': user,
        'tasks': tasks,
        'completed_count': completed_count,
        'total_count': total_count,
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "Utente eliminato con successo.")
    return redirect('accounts:admin_dashboard')
