from courses.models import Course
from timer.forms import TimeIntervalForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Allow the user to create a time interval ending at the time they push the button."""
    if request.method == 'POST':
        time_form = TimeIntervalForm(request.POST)
        # TODO use buttons
        if time_form.is_valid():
            time_form.save(commit=True)
            return render(request, 'courses/index.html')
        else:
            return render(request, 'timer/index.html', {'form': time_form})
    else:
        time_form = TimeIntervalForm()
        time_form.fields['course'].queryset = Course.objects.filter(user=request.user)  # only show this user's courses
        return render(request, 'timer/index.html', {'form': time_form})
