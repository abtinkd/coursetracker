from django.shortcuts import render
import time
from collections import namedtuple
from django.shortcuts import render, HttpResponse

# Create your views here.

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