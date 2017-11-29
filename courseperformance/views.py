from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from courseperformance.forms import CourseDateRangeForm
from timer.models import TimeInterval

import datetime
from datetime import datetime as dt
from django.forms.models import model_to_dict
from courses.models import Course


@login_required
def index(request):
    form = CourseDateRangeForm(user=request.user)
    if request.method == "POST":
        form = CourseDateRangeForm(request.POST, user=request.user)
        if form.is_valid():
            request.session.__setitem__('course_id', form.cleaned_data['course'].id)
            request.session.__setitem__('start_date', form.cleaned_data['start_date'])
            request.session.__setitem__('end_date', form.cleaned_data['end_date'])
            return display_course_performance(request)
    return render(request, 'courseperformance/index.html', {'course_date_form': form})


@login_required
def display_course_performance(request):
    """Display work done in the given time period in comparison with user-defined time goals."""
    course_id, start_date, end_date = request.session.__getitem__('course_id'), \
                                      request.session.__getitem__('start_date'), \
                                      request.session.__getitem__('end_date')

    # We have to process the dates, which were converted to strings when entered into session
    # Ensure we can't access the page without having defined a date range
    if course_id is None or start_date is None or end_date is None:
        return redirect('/courseperformance')

    course = Course.objects.get(pk=course_id)

    start_date = dt.strptime(start_date, '%m-%d-%Y')

    # Add one to end because we're about to round up - minimum interval is a day
    end_date = dt.strptime(end_date, '%m-%d-%Y').date()  # TODO integrate with function
    end_date_time = dt.combine(end_date, dt.max.time())

    #start = max(start_date_time, course.creation_time.replace(tzinfo=None))
    start = start_date_time

    end = end_date_time
    '''
    if course.activated is False:
        end = min(end_date_time, course.deactivation_time.replace(tzinfo=None))
    '''

    schedule_total_seconds = course.hours * (end - start).total_seconds() / (7 * 24)
    schedule_total_hours = schedule_total_seconds / 3600

    schedule_minutes, schedule_seconds = divmod(schedule_total_seconds, 60)
    schedule_hours, schedule_minutes = divmod(schedule_minutes, 60)

    schedule_hours = int(schedule_hours)
    schedule_minutes = int(schedule_minutes)
    schedule_seconds = int(schedule_seconds)


    # Don't include a Interval that have no intersection with the given range
    time_intervals = dict.fromkeys(TimeInterval.objects.filter(course__exact =course.id ,start_time__lte=end_date, end_time__gte=start_date))


    actual_total_seconds = 0
    for interval in time_intervals:
        start = max(start_date_time, interval.start_time.replace(microsecond=0, tzinfo=None))
        end = min(end_date_time, interval.end_time.replace(microsecond=0, tzinfo=None))
        interval_length = (end - start).total_seconds()
        interval.interval_length = interval_length

        actual_total_seconds += interval_length

    actual_minutes, actual_seconds = divmod(actual_total_seconds, 60)
    actual_hours, actual_minutes = divmod(actual_minutes, 60)

    actual_hours = int(actual_hours)
    actual_minutes = int(actual_minutes)
    actual_seconds = int(actual_seconds)

    content = {
                  'course_name': course.name,
                  'start_date': request.session.__getitem__('start_date'),
                  'end_date': request.session.__getitem__('end_date'),
                  'schedule_total_hours': schedule_total_hours,
                  'actual_hours': actual_hours,
                  'actual_minutes': actual_minutes,
                  'actual_seconds': actual_seconds,
                  'schedule_hours': schedule_hours,
                  'schedule_minutes': schedule_minutes,
                  'schedule_seconds': schedule_seconds,
                  'time_intervals': sorted(time_intervals.items(), key=lambda x: x[0].start_time)
                }

    return render(request, 'courseperformance/display.html', content)

