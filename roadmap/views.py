from datetime import timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from roadmap.models import Roadmap, TaskNode, UserTaskProgress


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'roadmap/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'roadmap/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    roadmap = Roadmap.objects.first()
    tasks = roadmap.nodes.all()

    completed_tasks = 0

    for task in tasks:
        progress, created = UserTaskProgress.objects.get_or_create(
            user=request.user,
            task=task
        )

        task.user_progress = progress
        task.deadline_warning = None

        if progress.is_completed:
            completed_tasks += 1

        if progress.deadline:
            now = timezone.now()

            if progress.deadline < now:
                task.deadline_warning = "⚠ Дедлайн просрочен!"
            elif progress.deadline <= now + timedelta(hours=24):
                task.deadline_warning = "⚠ Дедлайн скоро!"

    total_tasks = tasks.count()
    progress_percent = 0

    if total_tasks > 0:
        progress_percent = int((completed_tasks / total_tasks) * 100)

    completed_tasks_count = completed_tasks
    total_tasks_count = total_tasks

    return render(request, 'roadmap/dashboard.html', {
        'roadmap': roadmap,
        'tasks': tasks,
        'progress_percent': progress_percent,
        'completed_tasks_count': completed_tasks_count,
        'total_tasks_count': total_tasks_count,
    })


@login_required
def toggle_task(request, task_id):
    task = TaskNode.objects.get(id=task_id)

    progress, created = UserTaskProgress.objects.get_or_create(
        user=request.user,
        task=task
    )

    progress.is_completed = not progress.is_completed
    progress.save()

    return redirect('dashboard')


@login_required
def calendar_view(request):
    roadmap = Roadmap.objects.first()
    tasks = roadmap.nodes.all()

    events = []

    for task in tasks:
        progress, created = UserTaskProgress.objects.get_or_create(
            user=request.user,
            task=task
        )

        if progress.deadline:
            events.append({
                'title': task.title,
                'start': progress.deadline.isoformat(),
            })

    return render(request, 'roadmap/calendar.html', {
        'events': events,
    })