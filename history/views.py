import collections
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from timer.models import TimeInterval


@login_required
def index(request):  # TODO more time options
    """Expose an interface for seeing work done in the last week in comparison with user-defined time goals."""
    tallies = collections.defaultdict(int)  # time tallies
    start_time = datetime.datetime.now() - datetime.timedelta(days=7)  # one week ago
    for interval in TimeInterval.objects.filter(course__user=request.user, start_time__gte=start_time):
        tallies[interval.course] += (interval.end_time - interval.start_time).total_seconds() / 3600  # convert to hours
    # TODO expand for courses that are active but didn't have intervals
    return render(request, 'history/index.html', {'tallies': sorted(tallies.items(), key=lambda x: x[0].name)})
