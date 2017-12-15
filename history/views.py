from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from courses.models import Course
from .forms import HistoryForm
from .helper import *


@login_required
def index(request):
    """Display work done during a date range in comparison with user-defined time goals."""
    # Handle new date range / course view inputs
    form = HistoryForm(user=request.user)
    start_date, end_date, course = None, None, None
    if request.method == "POST":
        form = HistoryForm(data=handle_preset(request), user=request.user)
        if form.is_valid():
            start_date, end_date = form.cleaned_data['start_date'], form.cleaned_data['end_date']
            course = form.cleaned_data['course']

    # Retrieve relevant data
    start_date, end_date = process_dates(start_date, end_date)
    data = {'start_date': start_date.date(), 'end_date': end_date.date(), 'show_table': course is not None,
            'intervals': [], 'date_form': form}

    if data['show_table']:  # showing history for just one Course
        data['courses'] = [course]
        data['intervals'] = get_intervals(data['courses'][0], start_date, end_date)
    else:  # overall history - don't include Courses which weren't active during the given date range
        data['courses'] = list(Course.objects.filter(Q(user=request.user), Q(creation_time__lte=end_date),
                                                     Q(deactivation_time__isnull=True) | Q(deactivation_time__gte=start_date)))
    [compute_performance(course, start_date, end_date) for course in data['courses']]
    data['courses'] = sorted(data['courses'], reverse=True, key=lambda x: x.time_spent / x.total_target_hours)
    return render(request, 'history/index.html', data)
