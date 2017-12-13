from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from courses.models import Course
from .forms import HistoryForm
from timer.models import TimeInterval


@login_required
def index(request):
    form = HistoryForm(user=request.user)
    if request.method == "POST":
        if any([preset in request.POST for preset in ('year', 'month', 'week', 'current')]):
            data = {'end_date': timezone.datetime.today(),
                    'course': request.POST['course'] if 'course' in request.POST else None}
            if 'year' in request.POST:
                data['start_date'] = timezone.datetime.today() - relativedelta(years=+1)
            elif 'month' in request.POST:  # use relativedelta for accurate month calculations
                data['start_date'] = timezone.datetime.today() - relativedelta(months=+1)
            elif 'week' in request.POST:
                data['start_date'] = timezone.datetime.today() - timezone.timedelta(weeks=1)
            else:
                data['start_date'] = timezone.datetime.today()
                data['end_date'] = timezone.datetime.today() + timezone.timedelta(weeks=1)
            form = HistoryForm(data=data, user=request.user)
        else:  # custom range
            form = HistoryForm(request.POST, user=request.user)

        if form.is_valid():
            request.session['start_date'] = form.cleaned_data['start_date'].strftime('%m-%d-%Y')
            request.session['end_date'] = form.cleaned_data['end_date'].strftime('%m-%d-%Y')
            if form.cleaned_data['course']:
                request.session['course_id'] = form.cleaned_data['course'].id
            elif 'course_id' in request.session:
                del request.session['course_id']
            return display(request)
    return render(request, 'history/index.html', {'date_form': form})


@login_required
def display(request):
    """Display work done in the given time period in comparison with user-defined time goals."""
    # Ensure we can't access the page without having defined a date range
    if 'start_date' not in request.session or 'end_date' not in request.session:
        return redirect('/history')

    # We have to process the dates, which were converted to strings when entered into session
    start_date, end_date = process_dates(request)

    show_table = 'course_id' in request.session  # whether we're just showing history for a given course
    time_intervals = []
    if show_table:  # TODO refactor
        course = Course.objects.get(pk=request.session['course_id'])
        compute_performance(course, start_date, end_date)
        for interval in TimeInterval.objects.filter(course=course, start_time__gte=start_date,
                                                    end_time__lte=end_date).order_by('start_time'):
            interval.duration = (interval.end_time - interval.start_time).total_seconds() / 3600  # duration in hours
            time_intervals.append(interval)
    else:  # overall history - don't include Courses which weren't active during the given date range
        courses = list(Course.objects.filter(Q(user=request.user), Q(creation_time__lte=end_date),
                                             Q(deactivation_time__isnull=True) | Q(deactivation_time__gte=start_date)))
        for course in courses:
            compute_performance(course, start_date, end_date)

    return render(request, 'history/display.html',
                  {'courses': course if show_table else sorted(courses, reverse=True,
                                                               # sort in descending order by % complete
                                                               key=lambda x: x.time_spent / x.total_target_hours),
                   'start_date': start_date.date(), 'end_date': end_date.date(), 'show_table': show_table,
                   'intervals': time_intervals if show_table else None})


def process_dates(request):
    """Extract start and end dates from the request. Returns None, None if invalid request given."""
    start_date, end_date = timezone.datetime.strptime(request.session['start_date'], '%m-%d-%Y'), \
                           timezone.datetime.strptime(request.session['end_date'], '%m-%d-%Y')
    start_date, end_date = start_date.astimezone(timezone.get_current_timezone()), \
                           end_date.astimezone(timezone.get_current_timezone())
    return start_date, end_date.replace(hour=23, minute=59, second=59, microsecond=999)  # end date is inclusive


def compute_performance(course, start_date, end_date):
    """Given a Course and a date range, fill in performance information (time spent, target hours)."""
    start = max(start_date, course.creation_time.astimezone(timezone.get_current_timezone()))
    end = end_date if course.activated \
        else min(end_date, course.deactivation_time).astimezone(timezone.get_current_timezone())
    if (end - start).days < 1:  # minimum interval is a day
        end = start + timezone.timedelta(days=1)
    # Floor the given day
    start, end = start.replace(hour=0, minute=0, second=0, microsecond=0), \
                 end.replace(hour=0, minute=0, second=0, microsecond=0)

    # Multiply weekly hours by how many weeks passed while course was active
    course.total_target_hours = round(course.hours * (end - start).total_seconds() / 604800, 2)  # hours/week * weeks
    course.time_spent = sum([(interval.end_time - interval.start_time).total_seconds() / 3600  # convert to hours
                             for interval in TimeInterval.objects.filter(course=course, start_time__gte=start_date,
                                                                         end_time__lte=end_date)])
