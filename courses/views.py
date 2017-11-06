from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from courses.forms import *
from courses.models import Course
from courses.tables import CourseTable


@login_required
def index(request):
    """List the entered courses and ask the user for the name of the course they want to create."""
    create_form, edit_form, delete_form = CreateCourseForm(request.POST or None, user=request.user), \
                                          EditCourseForm(request.POST or None, user=request.user), \
                                          DeleteCourseForm(request.POST or None, user=request.user)

    if request.method == 'POST':
        if 'create' in request.POST and create_form.is_valid():
            create_form.save(commit=True)
            return redirect('/')
        elif 'edit' in request.POST and edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect('/')
        elif 'delete' in request.POST and delete_form.is_valid():
            delete_form.delete()
            return redirect('/')

    return render(request, 'courses/index.html',
                  {'table': CourseTable(Course.objects.filter(user=request.user).order_by('name')),
                   'create_form': create_form, 'edit_form': edit_form, 'delete_form': delete_form})
