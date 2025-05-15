import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404
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
from backend.accounts.models import Friendship

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

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)

    if to_user == request.user:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('profile', username=username)

    # Check if a request or friendship already exists
    existing = Friendship.objects.filter(
        from_user=request.user, to_user=to_user
    ).exists() or Friendship.objects.filter(
        from_user=to_user, to_user=request.user
    ).exists()

    if existing:
        messages.warning(request, "Friend request already sent or you're already friends.")
    else:
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f"Friend request sent to {to_user.username}.")

    return redirect('accounts:user_profile', username=username)

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    query = request.GET.get('q')
    if query:
        users = users.filter(username__icontains=query)
    else:
        users = []

    # Amici accettati
    friendships = Friendship.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        accepted=True
    )

    friends = [
        f.to_user if f.from_user == request.user else f.from_user
        for f in friendships
    ]

    completed_tasks_count = Task.objects.filter(user=request.user, completed_at__isnull=False).count()
    friends_count = len(friends)

    return render(request, 'accounts/online/user_list.html', {
        'users': users,
        'friends': friends,
        'completed_tasks_count': completed_tasks_count,
        'friends_count': friends_count,
    })

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    already_friends = Friendship.objects.filter(
        Q(from_user=request.user, to_user=profile_user) |
        Q(from_user=profile_user, to_user=request.user),
        accepted=True
    ).exists()

    pending_request = Friendship.objects.filter(
        Q(from_user=request.user, to_user=profile_user) |
        Q(from_user=profile_user, to_user=request.user),
        accepted=False
    ).first()

    can_accept = pending_request and pending_request.to_user == request.user

    # 🔢 Nuovo: conteggio task e amici del profilo visualizzato
    completed_tasks_count = Task.objects.filter(user=profile_user, completed_at__isnull=False).count()

    friendships = Friendship.objects.filter(
        Q(from_user=profile_user) | Q(to_user=profile_user),
        accepted=True
    )

    friends_count = friendships.count()

    return render(request, 'accounts/online/user_profile.html', {
        'profile_user': profile_user,
        'already_friends': already_friends,
        'pending': pending_request,
        'can_accept': can_accept,
        'completed_tasks_count': completed_tasks_count,
        'friends_count': friends_count,  # 👈 passalo al template
    })


@login_required
def accept_friend_request(request, username):
    from backend.accounts.models import Friendship
    from django.contrib.auth.models import User

    sender = get_object_or_404(User, username=username)

    friend_request = Friendship.objects.filter(
        from_user=sender,
        to_user=request.user,
        accepted=False
    ).first()

    if not friend_request:
        raise Http404("No valid friend request found.")

    friend_request.accepted = True
    friend_request.save()

    messages.success(request, f"You are now friends with {sender.username}!")
    return redirect('accounts:user_profile', username=sender.username)

