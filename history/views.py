from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from courses.models import Course
from .forms import HistoryForm
from .helper import *


@login_required
def index(request):
    """Display work done for a customizable date range in comparison with user-defined time goals."""
    # Handle new date range / course view inputs
    form = HistoryForm(user=request.user)
    if request.method == "POST":
        form = HistoryForm(data=handle_preset(request), user=request.user)
        if form.is_valid():
            request.session['start_date'] = form.cleaned_data['start_date'].strftime('%m-%d-%Y')
            request.session['end_date'] = form.cleaned_data['end_date'].strftime('%m-%d-%Y')
            if form.cleaned_data['course']:
                request.session['course_id'] = form.cleaned_data['course'].id
            elif 'course_id' in request.session:
                del request.session['course_id']  # delete the old Course data

    # Retrieve relevant data
    start_date, end_date = process_dates(request)  # the dates were converted to strings when entered into session

    data = {'start_date': start_date.date(), 'end_date': end_date.date(), 'show_table': 'course_id' in request.session,
            'intervals': [], 'date_form': form}

    if data['show_table']:  # showing history for just one Course
        data['courses'] = Course.objects.get(pk=request.session['course_id'])
        compute_performance(data['courses'], start_date, end_date)
        data['intervals'] = get_intervals(data['courses'], start_date, end_date)
    else:  # overall history - don't include Courses which weren't active during the given date range
        data['courses'] = list(Course.objects.filter(Q(user=request.user), Q(creation_time__lte=end_date),
                                                     Q(deactivation_time__isnull=True) | Q(deactivation_time__gte=start_date)))
        for course in data['courses']:
            compute_performance(course, start_date, end_date)
        data['courses'] = sorted(data['courses'], reverse=True, key=lambda x: x.time_spent / x.total_target_hours)
    return render(request, 'history/index.html', data)
