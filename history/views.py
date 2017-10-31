import datetime
from courses.models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from timer.models import TimeInterval


@login_required
def index(request):  # TODO more time options
    """Expose an interface for seeing work done in the last week in comparison with user-defined time goals."""
    tallies = dict.fromkeys(Course.objects.filter(user=request.user), 0)  # time tallies
    start_time = timezone.now() - datetime.timedelta(days=7)  # one week ago
    for interval in TimeInterval.objects.filter(course__user=request.user, start_time__gte=start_time):
        tallies[interval.course] += (interval.end_time - interval.start_time).total_seconds() / 3600  # convert to hours
    return render(request, 'history/index.html', {'tallies': sorted(tallies.items(), key=lambda x: x[0].name)})
