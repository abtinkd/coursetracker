from courses.models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from history.forms import DateRangeForm
from timer.models import TimeInterval


@login_required
def index(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            request.session.__setitem__('start_date', form.cleaned_data['start_date'])
            request.session.__setitem__('end_date', form.cleaned_data['end_date'])
            return display_history(request)
        else:
            return render(request, 'history/index.html', {'date_form': form})
    else:
        return render(request, 'history/index.html', {'date_form': DateRangeForm()})


@login_required
def display_history(request):
    """Display work done in the given time period in comparison with user-defined time goals."""
    # We have to process the dates, which were converted to strings when entered into session
    start_date, end_date = request.session.__getitem__('start_date'), request.session.__getitem__('end_date')
    if start_date is None or end_date is None:  # ensure we can't access the page without having defined a date range
        return redirect('/history')
    start_date, end_date = timezone.datetime.strptime(start_date, '%m-%d-%Y'), \
                           timezone.datetime.strptime(end_date, '%m-%d-%Y')

    weeks = (end_date - start_date).days / 7.0
    tallies = dict.fromkeys(Course.objects.filter(user=request.user), 0)  # time tallies  TODO preserve hours/week
    for course in tallies.keys():  # multiply by how many weeks passed
        course.hours *= weeks  # TODO make accurate to deactivation

    for interval in TimeInterval.objects.filter(course__user=request.user, start_time__gte=start_date,
                                                end_time__lte=end_date):
        tallies[interval.course] += (interval.end_time - interval.start_time).total_seconds() / 3600  # convert to hours

    return render(request, 'history/display.html', {'tallies': sorted(tallies.items(), key=lambda x: x[0].name),
                                                    'start_date': start_date, 'end_date': end_date})
