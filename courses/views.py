from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from courses.forms import *
from courses.models import Course
from courses.tables import CourseTable


@login_required
def index(request):
    """List the entered courses and ask the user for the name of the course they want to create."""
    course_table = CourseTable(Course.objects.filter(user=request.user).order_by('name'))  # only show this user's data
    if request.method == 'POST':
        print(request.POST)
        form = CourseForm(request.POST, user=request.user) if 'create' in request.POST \
            else EditCourseForm(request.POST, user=request.user)
        if form.is_valid():
            if 'delete' in request.POST:
                form.delete()  # delete the Course
            else:
                form.save(commit=True)  # save the Course data
            return redirect('/')
        else:
            return render(request, 'courses/index.html',
                          {'table': course_table,
                           'create_form': form if 'create' in request.POST else CourseForm(user=request.user),
                           'edit_form': form if 'edit' in request.POST else EditCourseForm(user=request.user)})
    else:
        return render(request, 'courses/index.html', {'table': course_table,
                                                      'create_form': CourseForm(user=request.user),
                                                      'edit_form': EditCourseForm(user=request.user)})
