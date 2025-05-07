from re import search
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import datetime
from django.utils import timezone
from .forms import TaskForm
from django.contrib.auth.models import User
from django.db.models import Count, Q

@login_required
def home(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.is_completed = False
            task.completed_at = None
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    # 🧠 Gestione ordinamento
    order_by = request.GET.get('order_by', 'created_at')
    order_dir = request.GET.get('order_dir', 'asc')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('q', '').strip()
    only_future = request.GET.get('only_future') == 'on'
    allowed_fields = ['priority', 'due_date', 'created_at', 'title']

    if order_by not in allowed_fields:
        order_by = 'created_at'

    ordering = order_by if order_dir == 'asc' else f'-{order_by}'

    # 📥 Query ordinata
    tasks_da_fare = Task.objects.filter(user=request.user, is_completed=False)

    if priority_filter in ['low', 'medium', 'high']:
        tasks_da_fare = tasks_da_fare.filter(priority=priority_filter)

    if only_future:
        tasks_da_fare = tasks_da_fare.filter(due_date__gte=datetime.today())

    if search_query:
        tasks_da_fare = tasks_da_fare.filter(title__icontains=search_query)

    tasks_da_fare = tasks_da_fare.order_by(ordering)

    tasks_fatti = Task.objects.filter(user=request.user, is_completed=True).order_by(ordering)

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
            login(request, user)  # login automatico dopo la registrazione
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
def admin_dashboard(request):
    query = request.GET.get('q', '')  # prende il valore della query

    users = User.objects.annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__is_completed=True))
    ).order_by('-date_joined')

    if query:
        users = users.filter(username__icontains=query)

    return render(request, 'todo/admin_dashboard.html', {
        'users': users,
        'query': query,
    })

@user_passes_test(lambda u: u.is_superuser)
def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'todo/user_tasks.html', {'user': user, 'tasks': tasks})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')