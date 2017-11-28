from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from courseperformance.forms import CourseDateRangeForm
from timer.models import TimeInterval
from courseperformance.tables import TimeIntervalTable
import datetime
from datetime import datetime as dt
from courses.models import Course


@login_required
def index(request):
    if request.method == "POST":
        form = CourseDateRangeForm(request.POST)

        if form.is_valid():
            request.session.__setitem__('course', form.cleaned_data['course'])
            request.session.__setitem__('start_date', form.cleaned_data['start_date'])
            request.session.__setitem__('end_date', form.cleaned_data['end_date'])
            return display_courseperformance(request)
        else:
            return render(request, 'courseperformance/index.html', {'date_form': form})
    else:
        return render(request, 'courseperformance/index.html', {'date_form': CourseDateRangeForm()})


@login_required
def display_courseperformance(request):
    """Display work done in the given time period in comparison with user-defined time goals."""


    course = request.session.__getitem__('course')
    start_date_str = request.session.__getitem__('start_date')
    end_date_str = request.session.__getitem__('end_date')


    # We have to process the dates, which were converted to strings when entered into session
    if start_date_str is None or end_date_str is None:  # ensure we can't access the page without having defined a date range
        return redirect('/courseperformance')

    start_date = dt.strptime(start_date_str, '%m-%d-%Y').date()

    # Add one to end because we're about to round up - minimum interval is a day
    end_date = dt.strptime(end_date_str, '%m-%d-%Y').date() + datetime.timedelta(days=1)

    # Don't include a Course that wasn't active for any of the given date range
    time_intervals = TimeInterval.objects.filter(course__exact =course.id ,start_time__lte=end_date, end_time__gte=start_date)

    start = max(start_date, course.creation_time.date())

    end = end_date
    if course.activated is False :
        end = min(end_date, course.deactivation_time.date())

    schedule_total_seconds = course.hours * (end - start).total_seconds() / (7*24)

    schedule_minutes, schedule_seconds = divmod(schedule_total_seconds, 60)
    schedule_hours, schedule_minutes = divmod(schedule_minutes, 60)


    actual_total_seconds = 0
    for interval in time_intervals:  # multiply by how many weeks passed while course existed and was activated
        start = max(start_date, interval.start_time)
        end = min(end_date, interval.end_time)
        actual_total_seconds += (end - start).total_seconds()

    actual_minutes, actual_seconds = divmod(actual_total_seconds, 60)
    actual_hours, actual_minutes = divmod(actual_minutes, 60)

    return render(request, 'courseperformance/display.html',
                          {
                              'course_name': course.name,
                              'start_date': request.session.__getitem__('start_date'),
                              'end_date': request.session.__getitem__('end_date'),

                              'actual_hours': actual_hours,
                              'actual_minutes': actual_minutes,
                              'actual_seconds': actual_seconds,
                              'schedule_hours': schedule_hours,
                              'schedule_minutes': schedule_minutes,
                              'schedule_seconds': schedule_seconds,

                              'table': TimeIntervalTable(TimeInterval.objects.filter(course=course, end_time__gte=start_date, start_time__lte=end_date).order_by('start_time')),
                          }
                  )


