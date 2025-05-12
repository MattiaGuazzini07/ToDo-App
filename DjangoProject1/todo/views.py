from re import search
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task, User, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import datetime
from django.utils import timezone
from .forms import TaskForm, UserForm
from django.db.models import Count, Q
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import HttpResponse
@login_required
def home(request):
    # Se l'utente non ha ancora un profilo, crealo al volo
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)
    # Gestione creazione nuova attività
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.is_completed = False
            task.completed_at = None
            task.save()
            messages.success(request, "✅ Attività creata con successo!")
            return redirect('home')
    else:
        form = TaskForm()

    # Filtri e ordinamento
    order_by = request.GET.get('order_by', 'created_at')
    order_dir = request.GET.get('order_dir', 'asc')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('q', '').strip()
    only_future = request.GET.get('only_future') == 'on'
    completed_filter = request.GET.get('completed')

    allowed_fields = ['priority', 'due_date', 'created_at', 'title']
    if order_by not in allowed_fields:
        order_by = 'created_at'

    ordering = order_by if order_dir == 'asc' else f'-{order_by}'

    # Base query
    tasks_da_fare = Task.objects.filter(user=request.user)

    # Filtro completati / da fare
    if completed_filter == "true":
        tasks_da_fare = tasks_da_fare.filter(is_completed=True)
    else:
        tasks_da_fare = tasks_da_fare.filter(is_completed=False)

    # Filtro per priorità
    if priority_filter in ['low', 'medium', 'high']:
        tasks_da_fare = tasks_da_fare.filter(priority=priority_filter)

    # Solo future
    if only_future:
        tasks_da_fare = tasks_da_fare.filter(due_date__gte=datetime.today())

    # Ricerca per titolo
    if search_query:
        tasks_da_fare = tasks_da_fare.filter(title__icontains=search_query)

    # Ordinamento
    tasks_da_fare = tasks_da_fare.order_by(ordering)

    # Task completati per sezione dedicata
    tasks_fatti = Task.objects.filter(user=request.user, is_completed=True).order_by(ordering)

    start_tour = request.GET.get("tour") == "1"

    return render(request, 'todo/home.html', {
        'form': form,
        'tasks_da_fare': tasks_da_fare,
        'tasks_fatti': tasks_fatti,
        'timestamp': datetime.now().timestamp(),
        'order_by': order_by,
        'order_dir': order_dir,
        'priority_filter': priority_filter,
        'search_query': search_query,
        'only_future': only_future,
        'completed_filter': completed_filter,
        'show_tour': not request.user.userprofile.has_seen_guide,
        'start_tour': start_tour,
    })



@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.completed_at = timezone.now()
    task.save()
    return redirect('home')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "🎉 Benvenuto su ToDo! Dai un'occhiata alla \t <a href='/guida/'><strong>guida introduttiva</strong></a> \t per iniziare 🔍",
            )

            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'todo/signup.html', {'form': form})

@login_required
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = False
    task.completed_at = None
    task.save()
    return redirect('home')


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
            return redirect('user_tasks', user_id=user.id)
    else:
        form = TaskForm()

    return render(request, 'todo/user_tasks.html', {
        'user': user,
        'tasks': tasks,
        'completed_count': completed_count,
        'total_count': total_count,
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Utente '{form.cleaned_data['username']}' creato con successo ✅")
                return redirect('admin_dashboard')
            except IntegrityError:
                form.add_error('username', 'Questo username è già in uso.')
    else:
        form = UserForm()

    users = User.objects.all()
    for user in users:
        user.total_tasks = Task.objects.filter(user=user).count()
        user.completed_tasks = Task.objects.filter(user=user, is_completed=True).count()

    return render(request, 'todo/admin_dashboard.html', {
        'form': form,
        'users': users,
        'total_users': users.count()
    })


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort_by", "username")

    allowed_sort_fields = ['username', '-username', 'email', '-email', 'date_joined', '-date_joined']
    if sort_by not in allowed_sort_fields:
        sort_by = 'username'

    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Utente '{form.cleaned_data['username']}' creato con successo ✅")
                return redirect('admin_dashboard')
            except IntegrityError:
                form.add_error('username', 'Questo username è già in uso.')
                messages.error(request, "Username già in uso.")
        else:
            messages.error(request, "Dati non validi.")

    pinned_email = "mattiaguazzini007@gmail.com"
    pinned_user = User.objects.filter(email=pinned_email).annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__is_completed=True))
    ).first()

    user_qs = User.objects.annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__is_completed=True))
    )

    if query:
        user_qs = user_qs.filter(username__icontains=query)

    user_qs = user_qs.exclude(email=pinned_email).order_by(sort_by)

    return render(request, 'todo/admin_dashboard.html', {
        'form': form,
        'pinned_user': pinned_user,
        'users': user_qs,
        'query': query,
        'sort_by': sort_by,
        'total_users': User.objects.count(),
    })


@login_required
def edit_task(request, task_id):
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task aggiornato con successo ✅")
            if request.user.is_superuser:
                return redirect('user_tasks', user_id=task.user.id)
            else:
                return redirect('home')
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})

@user_passes_test(lambda u: u.groups.filter(name='Staff').exists() or u.is_superuser)
def staff_dashboard(request):
    tasks = Task.objects.all().select_related('user').order_by('-created_at')

    users = User.objects.annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__is_completed=True))
    )

    return render(request, 'todo/staff_dashboard.html', {
        'tasks': tasks,
        'users': users,
        'total_tasks': tasks.count(),
        'total_users': User.objects.count(),
        'total_completed_tasks': tasks.filter(is_completed=True).count(),
        'total_incomplete_tasks': tasks.filter(is_completed=False).count(),
    })

@login_required
def calendar_view(request):
    return render(request, 'todo/calendar.html')

@login_required
def task_events(request):
    tasks = Task.objects.filter(user=request.user)
    events = []

    for task in tasks:
        if task.due_date:
            events.append({
                'title': task.title,
                'start': task.due_date.isoformat(),
                'color': get_color(task.priority),
                'url': f'/edit/{task.id}/'
            })
    return JsonResponse(events, safe=False)

def get_color(priority):
    return {
        'high': '#dc3545',
        'medium': '#ffc107',
        'low': '#28a745'
    }.get(priority, '#007bff')

@login_required
def guida_view(request):
    return render(request, 'todo/guida.html')

@require_POST
@login_required
def tour_seen(request):
    request.user.userprofile.has_seen_guide = True
    request.user.userprofile.save()
    return HttpResponse(status=204)