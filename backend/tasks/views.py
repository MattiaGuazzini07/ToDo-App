from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from datetime import datetime

from .models import Task
from .forms import TaskForm
from ..accounts.models import UserProfile


@login_required
def home(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    start_tour = request.GET.get("tour") == "1"
    show_tour = not request.user.userprofile.has_seen_guide

    form = TaskForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "✅ Attività creata con successo!")
        return redirect('tasks:home')

    # Qui leggiamo i filtri reali usati nel form
    search = request.GET.get('q') or ""
    priority = request.GET.get('priority') or ""
    completed = request.GET.get('completed')  # "true" | "false" | None

    queryset = Task.objects.filter(user=request.user)

    if completed == "true":
        queryset = queryset.filter(is_completed=True)
    elif completed == "false":
        queryset = queryset.filter(is_completed=False)

    if priority:
        queryset = queryset.filter(priority=priority)

    if search:
        queryset = queryset.filter(title__icontains=search)

    # Divisione finale
    tasks_da_fare = queryset.filter(is_completed=False)
    tasks_fatti = queryset.filter(is_completed=True)

    return render(request, 'tasks/user/home.html', {
        'form': form,
        'tasks_da_fare': tasks_da_fare,
        'tasks_fatti': tasks_fatti,
        'start_tour': start_tour,
        'show_tour': show_tour,
        'search_query': search,
        'priority_filter': priority,
        'completed_filter': completed,
    })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.completed_at = timezone.now()
    task.save()
    return redirect('tasks:home')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('tasks:home')

@login_required
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = False
    task.completed_at = None
    task.save()
    return redirect('tasks:home')

@login_required
def edit_task(request, task_id):
    # Se superuser può modificare qualunque task, altrimenti solo i propri
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task aggiornato con successo ✅")
            # Redirect logico: superuser torna alla pagina dell'utente, gli altri alla home
            if request.user.is_superuser:
                return redirect('accounts:user_tasks', user_id=task.user.id)
            return redirect('tasks:home')
    else:
        form = TaskForm(instance=task)

    # Template: mostra lo stesso a tutti
    return render(request, 'tasks/user/edit_task.html', {
        'form': form,
        'task': task,
    })

@login_required
def staff_dashboard(request):
    tasks = Task.objects.all().select_related('user').order_by('-created_at')
    return render(request, 'tasks/staff/staff_dashboard.html', {'tasks': tasks})

@login_required
def calendar_view(request):
    return render(request, "tasks/user/calendar.html")

@login_required
def task_events(request):
    tasks = Task.objects.filter(user=request.user)
    events = [
        {
            "title": t.title,
            "start": t.due_date.isoformat(),
            "color": _color(t.priority),
            "url": f"/tasks/edit/{t.id}/",
        }
        for t in tasks if t.due_date
    ]
    return JsonResponse(events, safe=False)

def _color(priority):
    return {
        "high": "#dc3545",
        "medium": "#ffc107",
        "low": "#28a745",
    }.get(priority, "#007bff")

@login_required
def guida_view(request):
    return render(request, "tasks/user/guida.html")

@login_required
def tour_seen(request):
    request.user.userprofile.has_seen_guide = True
    request.user.userprofile.save()
    return HttpResponse(status=204)
