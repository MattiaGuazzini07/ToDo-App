from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import datetime

@login_required
def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title, user=request.user)
            return redirect('home')  # ricarica la pagina

    tasks_da_fare = Task.objects.filter(user=request.user, completed=False)
    tasks_fatti = Task.objects.filter(user=request.user, completed=True)
    return render(request, 'todo/home.html', {
        'tasks_da_fare': tasks_da_fare,
        'tasks_fatti': tasks_fatti,
        'timestamp': datetime.now().timestamp()
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
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
            login(request, user)  # login automatico dopo la registrazione
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'todo/signup.html', {'form': form})

@login_required
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = False
    task.save()
    return redirect('home')