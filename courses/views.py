from courses.forms import *
from courses.models import Course
from courses.tables import CourseTable
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Allow viewing and manipulation of the user's Courses."""
    create_form, edit_form, delete_form = CreateCourseForm(user=request.user), EditCourseForm(user=request.user), \
                                          DeleteCourseForm(user=request.user)
    tab = 'create'

    if request.method == 'POST':
        for name, form in (('create', create_form), ('edit', edit_form), ('delete', delete_form)):
            if name in request.POST:  # reinitialize the form using POST data and mark which tab is active
                form, tab = form.Meta.__init__(request.POST, user=request.user), name
                if form.is_valid():  # do the corresponding operation
                    form.save(commit=True)
                    form = form.Meta.__init__(user=request.user)  # reset form so we can render the page anew
                    break

    return render(request, 'courses/index.html',
                  {'table': CourseTable(Course.objects.filter(user=request.user).order_by('name')),
                   'create_form': create_form, 'edit_form': edit_form, 'delete_form': delete_form, 'tab': tab})
