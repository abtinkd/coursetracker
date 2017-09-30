import time
from collections import namedtuple
from django.shortcuts import render, HttpResponse

# Create your views here.
# function based view
def home(request):
    name = "Tracker"
    args = {'name': name}
    return render(request, 'account/home.html', args)

def login(request):
    return render(request, 'account/login.html')

def createCourse(request):
    """Ask the user for the name of the course they want to create."""
    course_name = UI.getCourseName()  # TODO implement
    if course_name not in self.courses:
        self.courses.add(course_name)  # TODO where do we initialize this set?
    else:
        UI.display("Course name already exists.")

def startTimer(request):
    """Ask the user what course they're working on and then start the timer."""
    course_name = UI.getCourseChoice()  # TODO implement
    self.new_interval = namedtuple(course=course_name, start_time=time.time(), end_time=None)  # TODO store appropriately

def endTimer(request):
    """End the current timer.

    Assumes that startTimer() has been called
    """
    self.new_interval.end_time = time.time()
    # TODO send to sql database
    self.new_interval = None  # we're done with the most recently-recorded interval, so clear
