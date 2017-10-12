from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from courses.forms import CourseForm
from courses.models import Course


@login_required
def index(request):
    """List the entered courses and ask the user for the name of the course they want to create."""
    courses = Course.objects.order_by('name')
    if request.method == 'POST':
        name_form = CourseForm(request.POST)
        if name_form.is_valid():
            name_form.save(commit=True)
            return index(request)
        else:
            return render(request, 'courses/index.html', {'courses': courses, 'form': name_form})
    else:
        return render(request, 'courses/index.html', {'courses': courses, 'form': CourseForm()})
