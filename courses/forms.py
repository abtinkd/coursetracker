from django import forms
from courses.models import Course
from django.contrib.auth.models import User


class CourseForm(forms.ModelForm):
    """Creates a Form from the Course model."""
    name = forms.CharField(max_length=50, help_text='Please enter the course name.')
    hours = forms.IntegerField(min_value=1, help_text='Please enter how many hours you want to work on this each week.')

    def is_valid(self, user):
        """Checks if the user has already created an identically-named course, in addition to super().is_valid()."""
        if not super().is_valid():  # see if the form is otherwise valid
            return False

        try:  # finding an identically-named course belonging to this user
            Course.objects.filter(user=user).get(name=self.cleaned_data['name'])
        except Course.DoesNotExist:
            return True
        self.add_error('name', 'A course with this name already exists.')  # TODO always shows
        return False

    def save(self, user, commit):
        """Attach the user data and save to the database."""
        course = super().save(commit=False)
        course.user = user
        if commit:
            course.save()
        return course

    class Meta:
        model = Course

        fields = ('name', 'hours', )
        exclude = ('user', )  # we don't want to show them all users in the database
