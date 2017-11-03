from courses.models import Course
from timer.forms import TimeIntervalForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone


@login_required
def index(request):
    """Allow the user to create a time interval ending at the time they push the button."""
    if request.method == 'POST':
        start_time = request.session.__getitem__('start_time')
        time_form = TimeIntervalForm(request.POST,
                                     initial={'start_time': timezone.datetime.strptime(start_time, '%m-%d-%Y %H:%M:%S')})
        # TODO use buttons
        if time_form.is_valid():
            print(time_form.save(commit=True))
            return redirect('/courses')
        else:
            return render(request, 'timer/index.html', {'form': time_form})
    else:
        start_time = timezone.now()
        request.session.__setitem__('start_time', start_time.strftime('%m-%d-%Y %H:%M:%S'))
        time_form = TimeIntervalForm(initial={'start_time': start_time})
        # Only show active courses for this user
        time_form.fields['course'].queryset = Course.objects.filter(user=request.user, activated=True).order_by('name')
        return render(request, 'timer/index.html', {'form': time_form})
