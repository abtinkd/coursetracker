from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from courses.forms import *
from courses.models import Course


@login_required
def index(request):  # TODO show activation status
    """List the entered courses and ask the user for the name of the course they want to create."""
    courses = Course.objects.filter(user=request.user).order_by('name')  # only show this user's data TODO improve table
    if request.method == 'POST':
        form = CourseForm(request.POST) if 'create' in request.POST else EditCourseForm(request.POST)
        if form.is_valid(request.user):
            if 'delete' in request.POST:
                form.delete()
            else:
                form.save(request.user, commit=True)
            return redirect('/')
        else:
            return render(request, 'courses/index.html',
                          {'courses': courses,
                           'create_form': form if 'create' in request.POST else CourseForm(request.POST),
                           'edit_form': form if 'edit' in request.POST else EditCourseForm(request.POST)})
    else:
        edit_form = EditCourseForm()
        edit_form.fields['edit_course'].queryset = Course.objects.filter(user=request.user).order_by('name')
        return render(request, 'courses/index.html', {'courses': courses, 'create_form': CourseForm(),
                                                      'edit_form': edit_form})
