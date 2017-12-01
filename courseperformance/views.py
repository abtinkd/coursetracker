from courseperformance.forms import CourseDateRangeForm
from courseperformance.tables import TimeIntervalTable
from courses.models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from history.views import process_dates
from timer.models import TimeInterval


@login_required
def index(request):
    form = CourseDateRangeForm(user=request.user)
    if request.method == "POST":
        form = CourseDateRangeForm(request.POST, user=request.user)
        if form.is_valid():
            request.session.__setitem__('course_id', form.cleaned_data['course'].id)
            request.session.__setitem__('start_date', form.cleaned_data['start_date'].strftime('%m-%d-%Y'))
            request.session.__setitem__('end_date', form.cleaned_data['end_date'].strftime('%m-%d-%Y'))
            return display(request)
    return render(request, 'courseperformance/index.html', {'course_date_form': form})


@login_required
def display(request):
    """Display work done in the given time period in comparison with user-defined time goals."""
    # Ensure we can't access the page without having defined a date range
    if request.session.__getitem__('course_id') is None or request.session.__getitem__('start_date') is None or \
       request.session.__getitem__('end_date') is None:
        return redirect('/courseperformance')

    # We have to process the dates, which were converted to strings when entered into session
    start_date, end_date = process_dates(request)
    course = Course.objects.get(pk=request.session.__getitem__('course_id'))

    # Find start and end DateTimes for the Course
    start = max(start_date, course.creation_time.astimezone(timezone.get_current_timezone()))
    end = end_date if course.activated \
        else min(end_date, course.deactivation_time).astimezone(timezone.get_current_timezone())
    if (end - start).days < 1:  # minimum interval is a day
        end = start + timezone.timedelta(days=1)
    # Round to nearest day
    start, end = start.replace(hour=0, minute=0, second=0, microsecond=0), \
                 end.replace(hour=0, minute=0, second=0, microsecond=0)
    total_target_hours = course.hours * (end - start).total_seconds() / 604800  # hours/week * weeks

    # Don't include a Interval that have no intersection with the given range
    time_intervals = TimeInterval.objects.filter(course=course, start_time__lte=end_date,
                                                 end_time__gte=start_date).order_by('start_time')
    for time in time_intervals:
        time.length = (time.end_time - time.start_time).seconds / 3600  # in hours  TODO fix

    total_hours = sum([(time.end_time - time.start_time).seconds / 3600 for time in time_intervals])
    return render(request, 'courseperformance/display.html',
                  {'table': TimeIntervalTable(time_intervals),
                   'course_name': course.name,
                   'start_date': request.session.__getitem__('start_date'),
                   'end_date': request.session.__getitem__('end_date'),
                   'total_hours': total_hours, 'total_target_hours': total_target_hours})
