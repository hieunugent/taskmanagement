# tasks/tasks.py

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
from django.contrib.auth.models import User
from datetime import timedelta

@shared_task
def send_due_date_reminders():
    """Check for tasks with due dates in the next day and send reminders."""
    tomorrow = timezone.now().date() + timedelta(days=1)
    tasks_due_tomorrow = Task.objects.filter(due_date=tomorrow, completed=False)
    for task in tasks_due_tomorrow:
        assignee = task.assignee
        send_reminder_email(assignee.email, task)
        
def send_reminder_email(email, task):
    """Send a reminder email to the task assignee."""
    subject = f'Reminder: Task "{task.title}" Due Tomorrow'
    message = f'Hello, {task.assignee.username}! Just a reminder that your task "{task.title}" is due tomorrow ({task.due_date}). Please make sure to complete it on time.'
    from_email = 'henry09091188@gmail.com'  # Replace with your email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
