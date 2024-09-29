# tasks/forms.py
from django import forms
from .models import Task
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assignee', "due_date"]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})  # HTML5 date input
        }
    def __init__(self,*args, **kwargs):
        user= kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        if user.groups.filter(name='Can Assign to Others', ).exists():
            self.fields['assignee'].queryset=User.objects.all()
        else:
            self.fields['assignee'].queryset=User.objects.filter(id= user.id)
class ChartTypeForm(forms.Form):
    CHART_CHOICES = [
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart'),
    ]
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label="Select Chart Type")