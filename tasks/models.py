# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Task(models.Model):
     PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('O', 'Ongoing'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add =True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
def __str__(self):
    return self.title