# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
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
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task,user=request.user )
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