from django.shortcuts import render

# Create your views here.
def createCourse(request):
    """Ask the user for the name of the course they want to create."""
    course_name = UI.getCourseName()  # TODO implement
    if course_name not in self.courses:
        self.courses.add(course_name)  # TODO where do we initialize this set?
    else:
        UI.display("Course name already exists.")
