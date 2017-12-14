from dateutil.relativedelta import relativedelta
from django.utils import timezone
from timer.models import TimeInterval


def handle_preset(request):
    """If a preset has been selected, set dates appropriately and return the form data."""
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
        return data
    return request.POST  # custom range was selected


def process_dates(request):
    """Extract start and end dates from the request. Returns None, None if invalid request given."""
    if 'start_date' not in request.session or 'end_date' not in request.session:  # default range is this week
        start_date, end_date = timezone.datetime.today() - timezone.timedelta(weeks=1), timezone.datetime.today()
    else:
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


def get_intervals(course, start_date, end_date):
    """Annotate all intervals in the date range for the Course with duration information."""
    intervals = []
    for interval in TimeInterval.objects.filter(course=course, start_time__gte=start_date,
                                                end_time__lte=end_date).order_by('start_time'):
        minutes, seconds = divmod((interval.end_time - interval.start_time).total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)  # TODO check timezones work on Heroku
        interval.start_time = interval.start_time.astimezone(timezone.get_current_timezone())
        interval.duration = "{:2.0f}h:{:2.0f}m:{:2.0f}s".format(hours, minutes, seconds)
        intervals.append(interval)
    return intervals
