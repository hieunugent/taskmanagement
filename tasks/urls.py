# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),  # List all tasks
    path('create/', views.task_create, name='task-create'),  # Create a new task
    path('<int:pk>/update/', views.task_update, name='task-update'),  # Update an existing task
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),  # Delete a task
    path('supervisor',views.task_list_view, name='supervisor'),
    path('mycalendar',views.calendar_view, name='mycalendar'),
]
