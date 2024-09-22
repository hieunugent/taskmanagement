# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from calendar import monthrange
from .models import Task
from .forms import TaskForm
from datetime import date, timedelta
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    order_by = request.GET.get('order_by')
    group_by = request.GET.get('group_by')
    if order_by == 'due_date_asc':
        tasks = tasks.order_by('due_date')
    elif order_by == 'due_date_desc':
        tasks = tasks.order_by('-due_date')
    elif order_by == 'title_asc':
        tasks = tasks.order_by('title')
    elif order_by == 'title_desc':
        tasks = tasks.order_by('-title')
   
    if group_by == 'status':
        tasks = tasks.order_by('status')
    elif group_by == 'assignee':
        tasks = tasks.order_by('assignee')

    return render(request,'tasks/task_list.html', {'tasks': tasks, 'user':request.user})
@login_required
def group_list_status(request):
    tasks = Task.objects.filter(user=request.user)
    group_by = request.GET.get('group_by')
    if group_by == 'status':
        tasks = tasks.order_by('status')
    elif group_by == 'assignee':
        tasks = tasks.order_by('assignee')
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
def calendar_view(request, year=None,month=None):
    today = timezone.now().date()
    if year is None or month is None:
        year = today.year
        month = today.month
    else:
        year = int(year)
        month = int(month)
    # Get the first day of the month and number of days in the month
    first_day_of_month, days_in_month = monthrange(year, month)

    # Create a list of days in the current month
    days = [date(year, month, day) for day in range(1, days_in_month + 1)]
    # Get the previous and next months
    current_date = date(year, month, 1)
    prev_month = (current_date - timedelta(days=1)).replace(day=1)
    next_month = (current_date + timedelta(days=32)).replace(day=1)
    # Retrieve all tasks for the current month
    tasks = Task.objects.filter(due_date__year=year, due_date__month=month)

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
        'month': today.strftime('%B'),
        'year': year,
        'day_names': day_names, 
        'prev_year': prev_month.year,
        'prev_month': prev_month.month,
        'next_year': next_month.year,
        'next_month': next_month.month,
    }
    return render(request, 'calendarview/calendar.html', context)
@login_required
def task_list_search(request):
    query = request.GET.get('q')  # Get the search query from the GET request
    if query:
          tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(assignee__username__icontains=query)
        ).order_by('due_date') # Search by task name (case insensitive)
    else:
        tasks = Task.objects.all() 
        print(tasks) # If no search query, return all tasks
    context={
        'tasks': tasks,
        'query': query
    }
    return render(request, 'tasks/task_list_search.html', context)

@login_required
def task_list_instance_search(request):
    if request.is_ajax():
        query = request.GET.get('q', '')
        tasks = Task.objects.filter(title__icontains=query)
        results = []

        # Prepare the results in a format that JavaScript can understand (usually a list of dicts)
        for task in tasks:
            results.append({
                'title': task.title,
                'description': task.description,
            })
        return JsonResponse({'results': results})
    task_list_search(request)
    # If the request is not AJAX, render the search page normally
   