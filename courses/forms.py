from django import forms
from django.forms import ValidationError
from django.utils import timezone
from courses.models import Course
from timer.models import TimeInterval


class CreateCourseForm(forms.ModelForm):  # TODO make robust against scripts
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        """Make sure the user hasn't already created a course of this name."""
        if len(self.cleaned_data['name']) > 50:
            raise ValidationError('Course name cannot exceed 50 characters.')
        if Course.objects.filter(user=self.user, name=self.cleaned_data['name']).exists():
            raise ValidationError("Course already exists.")
        return self.cleaned_data['name']

    def clean_hours(self):  # TODO reuse?
        if self.cleaned_data['hours'] <= 0:
            raise ValidationError("Course hours must be greater than zero.")
        if self.cleaned_data['hours'] > 168:
            raise ValidationError("There are only 168 hours in a week!")
        return self.cleaned_data['hours']

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
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course to modify")
    name = forms.CharField(required=False)  # entering nothing will keep the name the same
    hours = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=self.user, activated=True).order_by('name')

    def clean_name(self):
        if len(self.cleaned_data['name']) > 50:
            raise ValidationError('Course name cannot exceed 50 characters.')
        return self.cleaned_data['name']

    def clean_hours(self):
        if self.cleaned_data['hours'] and self.cleaned_data['hours'] <= 0:
            raise ValidationError("Course hours must be greater than zero.")
        if self.cleaned_data['hours'] and self.cleaned_data['hours'] > 168:
            raise ValidationError("There are only 168 hours in a week!")
        return self.cleaned_data['hours']

    def clean(self):
        """Make sure the user hasn't already created a course of this name."""
        if 'name' in self.cleaned_data and Course.objects.filter(user=self.user, name=self.cleaned_data['name']).exists() and \
            self.cleaned_data["course"] != Course.objects.get(user=self.user, name=self.cleaned_data['name']):
            raise ValidationError("That Course name is already taken.")

    def save(self, commit):
        """Applies the edits to the selected course."""
        if self.cleaned_data['name']:  # don't change name if not specified
            self.cleaned_data["course"].name = self.cleaned_data['name']
        if 'activated' in self.changed_data and self.cleaned_data["course"].activated:  # course is being deactivated
            self.cleaned_data["course"].activated = self.cleaned_data['activated']
            self.cleaned_data["course"].deactivation_time = timezone.now()
        elif self.cleaned_data['hours']:  # only change hours if not being deactivated and has been specified
            self.cleaned_data["course"].hours = self.cleaned_data['hours']

        if commit:
            self.cleaned_data["course"].save()
        return self.cleaned_data["course"]

    class Meta:
        model = Course

        fields = ('course', 'name', 'hours', 'activated', )
        exclude = ('user', )  # we don't want to show them all users in the database


class DeleteCourseForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course to delete")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=self.user).order_by('name')

    def delete(self):
        """Delete the given course."""
        TimeInterval.objects.filter(course=self.cleaned_data["course"]).delete()
        self.cleaned_data["course"].delete()
