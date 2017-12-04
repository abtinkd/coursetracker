from courses.forms import *
from courses.models import Course
from courses.tables import CourseTable
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def index(request):  # TODO integration test
    """Allow viewing and manipulation of the user's Courses."""
    create_form, edit_form, delete_form = CreateCourseForm(user=request.user), EditCourseForm(user=request.user), \
                                          DeleteCourseForm(user=request.user)
    tab = 'create'

    if request.method == 'POST':
        if 'create' in request.POST:
            create_form = CreateCourseForm(request.POST, user=request.user)
            if create_form.is_valid():
                create_form.save(commit=True)
                create_form = CreateCourseForm(user=request.user)
        elif 'edit' in request.POST:
            edit_form, tab = EditCourseForm(request.POST, user=request.user), 'edit'
            if edit_form.is_valid():
                edit_form.save(commit=True)
                edit_form = EditCourseForm(user=request.user)
        elif 'delete' in request.POST:
            delete_form, tab = DeleteCourseForm(request.POST, user=request.user), 'delete'
            if delete_form.is_valid():
                delete_form.delete()
                delete_form = DeleteCourseForm(user=request.user)

    return render(request, 'courses/index.html',
                  {'table': CourseTable(Course.objects.filter(user=request.user).order_by('name')),
                   'create_form': create_form, 'edit_form': edit_form, 'delete_form': delete_form, 'tab': tab})
