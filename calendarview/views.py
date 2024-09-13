from django.shortcuts import render
from datetime import date, timedelta

# Sample tasks
tasks = {
    "2024-09-14": ["Meeting with team", "Submit project report"],
    "2024-09-18": ["Doctor's appointment"],
    "2024-09-21": ["Family dinner"],
}

def calendar_view(request):
    # Generate days for the current month
    today = date.today()
    start_date = date(today.year, today.month, 1)
    days_in_month = (start_date.replace(month=start_date.month % 12 + 1) - timedelta(days=1)).day
    days = [(start_date + timedelta(days=i)).isoformat() for i in range(days_in_month)]

    # Pass tasks and days to the template
    context = {'days': days, 'tasks': tasks}
    return render(request, 'calendarview/calendar.html', context)
