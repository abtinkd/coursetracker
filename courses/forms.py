from django import forms
from django.forms import ValidationError
from django.utils import timezone
from courses.models import Course
from timer.models import TimeInterval


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        """Make sure the user hasn't already created a course of this name."""
        if Course.objects.filter(user=self.user, name=self.cleaned_data['name']).exists():
            raise ValidationError("Course already exists.")
        return self.cleaned_data['name']

    def save(self, commit):
        """Attach the user data and save to the database."""
        course = super().save(commit=False)
        course.user = self.user
        if commit:
            course.save()
        return course

    class Meta:
        model = Course

        fields = ('name', 'hours', )
        exclude = ('activated', 'user', )  # we don't want to show them all users in the database


class EditCourseForm(forms.ModelForm):
    edit_course = forms.ModelChoiceField(queryset=Course.objects.filter(), label="Course to modify")
    name = forms.CharField(required=False)  # entering nothing will keep the name the same

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['edit_course'].queryset = Course.objects.filter(user=self.user).order_by('name')

    def clean(self):
        """Make sure the user hasn't already created a course of this name."""
        name = self.cleaned_data['name']
        if Course.objects.filter(user=self.user, name=name).exists() and \
            self.cleaned_data['edit_course'] != Course.objects.get(user=self.user, name=name):
            raise ValidationError("That Course name is already taken.")

    def delete(self):
        """Delete the given course."""
        TimeInterval.objects.filter(course=self.cleaned_data['edit_course']).delete()
        self.cleaned_data['edit_course'].delete()

    def save(self, commit):
        """Applies the edits to the selected course."""
        if self.cleaned_data['name']:  # don't change name if not specified
            self.cleaned_data['edit_course'].name = self.cleaned_data['name']
        if 'activated' in self.changed_data and self.cleaned_data['edit_course'].activated:  # course is being deactivated
            self.cleaned_data['edit_course'].activated = self.cleaned_data['activated']
            self.cleaned_data['edit_course'].deactivation_time = timezone.now()
        else:  # only change hours if not being deactivated
            self.cleaned_data['edit_course'].hours = self.cleaned_data['hours']

        if commit:
            self.cleaned_data['edit_course'].save()
        return self.cleaned_data['edit_course']

    class Meta:
        model = Course

        fields = ('name', 'hours', 'activated', )
        exclude = ('user', )  # we don't want to show them all users in the database
