import timer.models
from django.shortcuts import render, HttpResponse


def start(request):
    """Ask the user what course they're working on and then start the timer."""
    course_name = UI.getCourseChoice()  # TODO implement
    self.new_interval = TimeInterval()  # TODO what if user has left?
    self.new_interval = namedtuple(course=course_name, start_time=time.time(), end_time=None)  # TODO store appropriately


def end(request):
    """End the current timer.

    Assumes that start() has been called
    """
    if request.method == 'POST':
        #new_interval =
        new_interval.end_time = datetime.today()
        new_interval.save(commit=True)
        return render(request, 'courses')  # TODO go to courses screen?

    return render(request, 'timer')
