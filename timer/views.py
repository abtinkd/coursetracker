from courses.models import Course
from history.views import index as history_index
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
            return history_index(request)
        else:
            return render(request, 'timer/index.html', {'form': time_form})
    else:
        time_form = TimeIntervalForm()
        # Only show active courses for this user
        time_form.fields['course'].queryset = Course.objects.filter(user=request.user, activated=True).order_by('name')
        return render(request, 'timer/index.html', {'form': time_form})
