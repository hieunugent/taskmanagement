# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from calendar import monthrange
from .models import Task
from .forms import TaskForm
from datetime import date, timedelta


# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request,'tasks/task_list.html', {'tasks': tasks, 'user':request.user})

@login_required
def task_create(request):
    # user = request.user
    if request.method =='POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task Create Successfully')
            return redirect('task-list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form':form})

@login_required
def task_update(request, pk):
    """View to update an existing task."""
    task = get_object_or_404(Task, pk=pk)
    if task.user != request.user and task.assignee != request.user:
        return HttpResponseForbidden("You are not allowed to edit this task.")
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task-list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    """View to delete an existing task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task-list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
# views.py

@login_required
def task_list_view(request):
    # If the user is a superuser, display all tasks
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        # Otherwise, display only the tasks assigned to the current user
        tasks = Task.objects.filter(assignee=request.user)

    context = {
        'tasks': tasks,
    }
    return render(request, 'tasks/all_task_list.html', context)
@login_required
def calendar_view(request):
    today = timezone.now().date()
    current_year = today.year
    current_month = today.month
    # Get the first day of the month and number of days in the month
    first_day_of_month, days_in_month = monthrange(current_year, current_month)

    # Create a list of days in the current month
    days = [date(current_year, current_month, day) for day in range(1, days_in_month + 1)]

    # Retrieve all tasks for the current month
    tasks = Task.objects.filter(due_date__year=current_year, due_date__month=current_month)

    # Create a dictionary to hold tasks by day
    tasks_by_day = {day: [] for day in days}
    for task in tasks:
        tasks_by_day[task.due_date].append(task)

    # Prepare the calendar grid (weeks with 7 days each)
    weeks = []
    week = []
    # Fill the empty days before the first day of the month
    for _ in range(first_day_of_month):
        week.append(None)
    
    # Fill the days in the month
    for day in days:
        week.append(day)
        if len(week) == 7:
            weeks.append(week)
            week = []

    # Fill the remaining days of the last week
    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    context = {
        'user_name':request.user,
        'weeks': weeks,
        'tasks_by_day': tasks_by_day,
        'current_month': today.strftime('%B'),
        'current_year': current_year,
        'day_names': day_names, 
    }
    return render(request, 'calendarview/calendar.html', context)