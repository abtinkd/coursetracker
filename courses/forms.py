from courses.models import Course
from django import forms
from django.forms import ValidationError
from django.utils import timezone
from django.utils.html import strip_tags


class CreateCourseForm(forms.ModelForm):
    name = forms.CharField(label="Course name")
    hours = forms.IntegerField(label="Goal (hours per week)")
    char_limit = 25

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self, check_exists=True):
        """Make sure the user hasn't already created a course of this name."""
        if len(self.cleaned_data['name']) > self.char_limit:
            raise ValidationError('Course name cannot exceed {} characters.'.format(self.char_limit))
        if check_exists and Course.objects.filter(user=self.user, name=self.cleaned_data['name']).exists():
            raise ValidationError("Course already exists.")
        self.cleaned_data['name'] = strip_tags(self.cleaned_data['name'])
        return self.cleaned_data['name']

    def clean_hours(self):
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


class EditCourseForm(CreateCourseForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course to modify")
    name = forms.CharField(required=False, label="Course name")  # entering nothing will keep the name the same
    hours = forms.IntegerField(required=False, label="Goal (hours per week)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=self.user, activated=True).order_by('name')

    def clean_name(self):
        return super().clean_name(check_exists=False)

    def clean_hours(self):
        if self.cleaned_data['hours'] is not None:
            return super().clean_hours()

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

    def save(self, commit):
        """Delete the given course."""
        if commit:
            self.cleaned_data["course"].delete()
