from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from ..accounts.models import UserProfile


@login_required
def home(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "✅ Attività creata con successo!")
            return redirect('home')
    else:
        form = TaskForm()

    tasks_da_fare = Task.objects.filter(user=request.user)
    tasks_fatti = Task.objects.filter(user=request.user, is_completed=True)
    # Filtri e ordinamenti

    return render(request, 'tasks/home.html', {
        'form': form,
        'tasks_da_fare': tasks_da_fare,
        'tasks_fatti': tasks_fatti,
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


@login_required
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = False
    task.completed_at = None
    task.save()
    return redirect('home')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task aggiornato con successo ✅")
            return redirect('home')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


@login_required
def staff_dashboard(request):
    tasks = Task.objects.all().select_related('user').order_by('-created_at')
    return render(request, 'tasks/staff_dashboard.html', {'tasks': tasks})
