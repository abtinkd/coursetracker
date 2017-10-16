from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from courses.forms import CourseForm
from courses.models import Course


@login_required
def index(request):
    """List the entered courses and ask the user for the name of the course they want to create."""
    courses = Course.objects.filter(user=request.user).order_by('name')  # only show this user's data
    if request.method == 'POST':
        name_form = CourseForm(request.POST)
        if name_form.is_valid(request):
            name_form.save(request, commit=True)
            return index(request)
        else:
            return render(request, 'courses/index.html', {'courses': courses, 'form': name_form})
    else:
        return render(request, 'courses/index.html', {'courses': courses, 'form': CourseForm()})
