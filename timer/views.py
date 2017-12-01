from timer.models import TimeInterval
from timer.forms import CourseSelectionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone


@login_required
def index(request):
    """Allow the user to create a TimeInterval."""
    if request.method == 'POST':
        if 'start_time' in request.POST:  # get start_time from JS
            request.session.__setitem__('start_time', request.POST.get('start_time'))
            return render(request, 'timer/index.html')
        else:  # time to create the TimeInterval - user pressed 'Stop'
            form = CourseSelectionForm(request.POST, user=request.user)
            if form.is_valid():
                course = form.cleaned_data['course']
                start_time = timezone.datetime.strptime(request.session.__getitem__('start_time'), '%m-%d-%Y %H:%M:%S')
                if not start_time.tzinfo:
                    start_time = start_time.replace(tzinfo=timezone.get_current_timezone())
                start_time = start_time.astimezone(tz=timezone.utc)  # for use in database
                TimeInterval.objects.create(course=course, start_time=start_time)
                return redirect('/courses')
            else:
                return render(request, 'timer/index.html', {'form': form})
    else:
        return render(request, 'timer/index.html', {'form': CourseSelectionForm(user=request.user)})
