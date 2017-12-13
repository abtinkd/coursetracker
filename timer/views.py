from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from timer.models import TimeInterval
from timer.forms import CourseSelectionForm
from tracker.helper import already_submitted


@login_required
def index(request):
    """Allow the user to create a TimeInterval."""
    form = CourseSelectionForm(user=request.user)
    if request.method == 'POST':
        if 'start_time' in request.POST:  # get start_time from JS
            request.session['start_time'] = request.POST.get('start_time')
            return render(request, 'timer/index.html')
        else:  # time to create the TimeInterval - user pressed 'Stop'
            form = CourseSelectionForm(request.POST, user=request.user)
            # Make sure the user hasn't tried to submit this TimeInterval already
            if form.is_valid() and not already_submitted(request, request.session['start_time']):
                start_time = parser.parse(request.session['start_time'])
                if not start_time.tzinfo:
                    start_time = start_time.astimezone(timezone.get_current_timezone())
                TimeInterval.objects.create(course=form.cleaned_data['course'], start_time=start_time)
                return redirect('/courses')
    return render(request, 'timer/index.html', {'form': form})
