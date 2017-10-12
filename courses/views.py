from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from courses.forms import CourseForm
from courses.models import Course


def index(request):
    """List the entered courses."""
    course_list = Course.objects.order_by('-name')
    output = ', '.join([course.name for course in course_list])
    return HttpResponse(output)


def add_course(request):
    """Ask the user for the name of the course they want to create."""
    if request.method == 'POST':
        name_form = CourseForm(request.POST)
        if name_form.is_valid():
            name_form.save(commit=True)
            return index(request)
        else:
            print(name_form.errors)
    else:
        name_form = CourseForm()

    return render(request, 'courses/add_course.html', {'form': name_form})
