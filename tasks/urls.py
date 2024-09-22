# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.task_list, name='task-list'),  # List all tasks
    path('search/', views.task_list_search, name='task-list-search'),
    path('searchQ/', views.task_list_instance_search, name='task-list-search-instance'),
    path('create/', views.task_create, name='task-create'),  # Create a new task
    path('<int:pk>/update/', views.task_update, name='task-update'),  # Update an existing task
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),  # Delete a task
    path('supervisor',views.task_list_view, name='supervisor'),
    path('mycalendar',views.calendar_view, name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/',views.calendar_view, name="mycalendar")
]
