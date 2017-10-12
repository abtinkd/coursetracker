from django import forms
from courses.models import Course


class CourseForm(forms.ModelForm):
    """A helper class for creating a Form from the Course model."""
    name = forms.CharField(max_length=50, help_text='Please enter the course name.')
    hours = forms.IntegerField(min_value=1, help_text='Please enter how many hours you want to work on this each week.')

    class Meta:
        model = Course

        fields = ('name', 'hours', )
