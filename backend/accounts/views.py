import os, json
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .forms import UserForm, UserSettingsForm, TeamForm, InviteMemberForm
from .models import UserProfile, Friendship, Team, TeamMembership
from backend.tasks.models import Task, TeamTask
from backend.tasks.forms import TaskForm, TeamTaskForm
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

@login_required
def team_list(request):
    memberships = TeamMembership.objects.filter(user=request.user).select_related('team')

    # Form team task
    team_task_form = TeamTaskForm(request.POST or None, prefix='teamtask', user=request.user)

    # Form creazione team
    team_form = TeamForm(request.POST or None, prefix='team')

    if request.method == 'POST':
        if 'teamtask-title' in request.POST:  # identificazione tramite prefix
            if team_task_form.is_valid():
                team_task = team_task_form.save(commit=False)
                team_task.created_by = request.user
                team_task.save()
                team_task_form.save_m2m()
                messages.success(request, "✅ Task assegnata ai team.")
                return redirect('accounts:team_list')

        elif 'team-name' in request.POST:  # campo del TeamForm
            if team_form.is_valid():
                team = team_form.save(commit=False)
                team.owner = request.user
                team.save()
                TeamMembership.objects.create(user=request.user, team=team, role='admin')
                messages.success(request, f"✅ Team '{team.name}' creato!")
                return redirect('accounts:team_list')

    return render(request, 'accounts/online/team/team_list.html', {
        'memberships': memberships,
        'team_form': team_form,
        'team_task_form': team_task_form
    })

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if not TeamMembership.objects.filter(user=request.user, team=team).exists():
        return redirect('accounts:team_list')

    is_admin = TeamMembership.objects.filter(user=request.user, team=team, role='admin').exists()

    # Annotazioni task per ogni membro
    members = TeamMembership.objects.filter(team=team).select_related('user').annotate(
    created_tasks_count=Count('user__teamtask', filter=Q(user__teamtask__teams=team), distinct=True),
    completed_tasks_count=Count('user__team_completed_tasks', filter=Q(user__team_completed_tasks__teams=team),distinct=True)
    )


    team_tasks = TeamTask.objects.filter(teams=team).order_by('-created_at')
    completed_count = team_tasks.filter(is_completed=True).count()
    member_labels = [m.user.username for m in members]
    member_completati = [m.completed_tasks_count for m in members]

    form = InviteMemberForm(request.POST or None)
    new_task_form = TeamTaskForm()

    if request.method == 'POST':
        if 'username' in request.POST and is_admin:
            if form.is_valid():
                username = form.cleaned_data['username']
                role = form.cleaned_data['role']

                try:
                    user_to_add = User.objects.get(username=username)
                except User.DoesNotExist:
                    messages.error(request, "Utente non trovato.")
                    return redirect('accounts:team_detail', pk=pk)

                if TeamMembership.objects.filter(team=team, user=user_to_add).exists():
                    messages.warning(request, f"{username} è già nel team.")
                else:
                    TeamMembership.objects.create(team=team, user=user_to_add, role=role)
                    messages.success(request, f"{username} è stato aggiunto al team come {role}.")
                return redirect('accounts:team_detail', pk=pk)

        else:
            new_task_form = TeamTaskForm(request.POST)
            if new_task_form.is_valid():
                task = new_task_form.save(commit=False)
                task.created_by = request.user
                task.save()
                task.teams.add(team)
                messages.success(request, "Nuova attività creata con successo.")
                return redirect('accounts:team_detail', pk=pk)
            else:
                messages.error(request, "Errore nella creazione del task. Controlla i dati.")

    return render(request, 'accounts/online/team/team_detail.html', {
        'team': team,
        'members': members,
        'form': form,
        'team_tasks': team_tasks,
        'is_admin': is_admin,
        'new_task_form': new_task_form,
        'completed_count': completed_count,  # 👈 per Chart.js
        'member_labels': member_labels,
        'member_completati': member_completati,
    })

@login_required
def user_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[:5]
        results = [
            {
                'username': user.username,
                'avatar': user.userprofile.avatar  # se usi avatar nel profilo
            }
            for user in users
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def delete_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        raise Http404("Questo team non esiste o è già stato eliminato.")

    if not TeamMembership.objects.filter(user=request.user, team=team, role='admin').exists():
        return HttpResponseForbidden("Non sei autorizzato a eliminare questo team.")

    team.delete()
    return redirect('accounts:team_list')

@login_required
def leave_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    membership = TeamMembership.objects.filter(user=request.user, team=team).first()

    if membership:
        membership.delete()

    return redirect('accounts:team_list')

@login_required
def remove_from_team(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    is_admin = TeamMembership.objects.filter(team=team, user=request.user, role="admin").exists()

    if not is_admin:
        messages.error(request, "Non sei autorizzato a rimuovere membri dal team.")
        return redirect("accounts:team_detail", pk=team_id)

    if request.method == "POST":
        member = TeamMembership.objects.filter(team=team, user_id=user_id).first()
        if not member:
            messages.error(request, "Membro non trovato.")
        elif member.user == request.user:
            messages.warning(request, "Non puoi rimuovere te stesso.")
        else:
            member.delete()
            messages.success(request, f"{member.user.username} è stato rimosso dal team.")

    return redirect("accounts:team_detail", pk=team_id)