from courses.forms import *
from courses.models import Course
from courses.tables import CourseTable
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def index(request):
    """List the entered courses and ask the user for the name of the course they want to create."""
    create_form, edit_form, delete_form = CreateCourseForm(user=request.user), EditCourseForm(user=request.user), \
                                          DeleteCourseForm(user=request.user)

    if request.method == 'POST':
        if 'create' in request.POST:
            create_form = CreateCourseForm(request.POST, user=request.user)
            if create_form.is_valid():
                create_form.save(commit=True)
                return redirect('/courses')
        elif 'edit' in request.POST:
            edit_form = EditCourseForm(request.POST, user=request.user)
            if edit_form.is_valid():
                edit_form.save(commit=True)
                return redirect('/courses')
        elif 'delete' in request.POST:
            delete_form = DeleteCourseForm(request.POST, user=request.user)
            if delete_form.is_valid():
                delete_form.delete()
                return redirect('/courses')

    return render(request, 'courses/index.html',
                  {'table': CourseTable(Course.objects.filter(user=request.user).order_by('name')),
                   'create_form': create_form, 'edit_form': edit_form, 'delete_form': delete_form})
