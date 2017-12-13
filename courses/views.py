from courses.forms import *
from courses.models import Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """Allow viewing and manipulation of the user's Courses."""
    forms = {'create': CreateCourseForm(user=request.user), 'edit': EditCourseForm(user=request.user),
             'delete': DeleteCourseForm(user=request.user)}
    tab = 'create'

    if request.method == 'POST':
        for name in forms.keys():
            if name in request.POST:  # reinitialize the form using POST data and mark which tab is active
                forms[name], tab = forms[name].__class__(request.POST, user=request.user), name
                if forms[name].is_valid():  # do the corresponding operation
                    forms[name].save(commit=True)
                    forms[name] = forms[name].__class__(user=request.user)  # reset form so we can render the page anew
                break

    return render(request, 'courses/index.html',
                  {'courses': Course.objects.filter(user=request.user).order_by('name'), 'tab': tab,
                   'create_form': forms['create'], 'edit_form': forms['edit'], 'delete_form': forms['delete']})
