from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from courses.models import Course
from history.forms import DateRangeForm
from timer.models import TimeInterval


@login_required
def index(request):
    form = DateRangeForm()
    if request.method == "POST":
        if any([preset in request.POST for preset in ('year', 'month', 'week', 'current')]):
            data = {'end_date': timezone.datetime.today()}
            if 'year' in request.POST:
                data['start_date'] = timezone.datetime.today() - relativedelta(years=+1)
            elif 'month' in request.POST:  # use relativedelta for accurate month calculations
                data['start_date'] = timezone.datetime.today() - relativedelta(months=+1)
            elif 'week' in request.POST:
                data['start_date'] = timezone.datetime.today() - timezone.timedelta(weeks=1)
            elif 'current' in request.POST:
                data['start_date'] = timezone.datetime.today()
                data['end_date'] = timezone.datetime.today() + timezone.timedelta(weeks=1)
            form = DateRangeForm(data=data)
        else:  # custom range
            form = DateRangeForm(request.POST)

        if form.is_valid():
            request.session.__setitem__('start_date', form.cleaned_data['start_date'].strftime('%m-%d-%Y'))
            request.session.__setitem__('end_date', form.cleaned_data['end_date'].strftime('%m-%d-%Y'))
            return display(request)
    return render(request, 'history/index.html', {'date_form': form})


@login_required
def display(request):
    """Display work done in the given time period in comparison with user-defined time goals."""
    # Ensure we can't access the page without having defined a date range
    if request.session.__getitem__('start_date') is None or request.session.__getitem__('end_date') is None:
        return redirect('/history')

    # We have to process the dates, which were converted to strings when entered into session
    start_date, end_date = process_dates(request)

    # Don't include a Course that wasn't active for any of the given date range
    courses = list(Course.objects.filter(Q(user=request.user), Q(creation_time__lte=end_date),
                                         Q(deactivation_time__isnull=True) | Q(deactivation_time__gte=start_date)))
    for course in courses:  # multiply by how many weeks passed while course existed and was activated
        start = max(start_date, course.creation_time.astimezone(timezone.get_current_timezone()))
        end = end_date if course.activated \
              else min(end_date, course.deactivation_time).astimezone(timezone.get_current_timezone())
        if (end - start).days < 1:  # minimum interval is a day
            end = start + timezone.timedelta(days=1)
        # Round to nearest day
        start, end = start.replace(hour=0, minute=0, second=0, microsecond=0), \
                     end.replace(hour=0, minute=0, second=0, microsecond=0)

        course.total_target_hours = course.hours * (end - start).total_seconds() / 604800  # hours/week * weeks
        course.time_spent = sum([(interval.end_time - interval.start_time).total_seconds() / 3600  # convert to hours
                                 for interval in TimeInterval.objects.filter(course=course, start_time__gte=start_date,
                                                                             end_time__lte=end_date)])
        course.proportion_complete = course.time_spent / course.total_target_hours

    return render(request, 'history/display.html', {'courses': sorted(courses, reverse=True,
                                                                      key=lambda x: x.proportion_complete),
                                                    'start_date': start_date, 'end_date': end_date})


def process_dates(request):
    """Extract start and end dates from the request. Returns None, None if invalid request given."""
    start_date, end_date = request.session.__getitem__('start_date'), request.session.__getitem__('end_date')
    start_date, end_date = timezone.datetime.strptime(start_date, '%m-%d-%Y'), \
                           timezone.datetime.strptime(end_date, '%m-%d-%Y')
    start_date = start_date.replace(tzinfo=timezone.get_current_timezone())
    end_date = end_date.replace(tzinfo=timezone.get_current_timezone())
    return start_date, end_date.replace(hour=23, minute=59, second=59, microsecond=999)  # end date is inclusive
