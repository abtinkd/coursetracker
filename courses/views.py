from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.shortcuts import render
from courses.forms import CourseForm
from courses.models import Course


class CourseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.order_by('name')  # TODO embed so page can display currently-created classes
        return context

@login_required
def index(request):
    """List the entered courses and ask the user for the name of the course they want to create."""
    if request.method == 'POST':
        name_form = CourseForm(request.POST)
        if name_form.is_valid():
            name_form.save(commit=True)
            return index(request)
        else:
            return render(request, 'courses/index.html', {'form': name_form})
    else:
        return render(request, 'courses/index.html', {'form': CourseForm()})
