from django import forms
from courses.models import Course
from timer.models import TimeInterval


class CourseForm(forms.ModelForm):
    def is_valid(self, user):
        """Checks if the user has already created an identically-named course, in addition to super().is_valid()."""
        if not super().is_valid():  # see if the form is otherwise valid
            return False

        try:  # finding an identically-named course belonging to this user
            Course.objects.filter(user=user).get(name=self.cleaned_data['name'])
        except Course.DoesNotExist:
            return True  # TODO show error?
        else:
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
        exclude = ('activated', 'user', )  # we don't want to show them all users in the database


class EditCourseForm(forms.ModelForm):
    edit_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course to modify")
    name = forms.CharField(required=False)  # entering nothing will keep the name the same

    def is_valid(self, user):
        """If renaming, also checks if the user has already created an identically-named course."""
        if not super().is_valid():  # see if the form is otherwise valid
            return False
        if 'name' not in self.changed_data:  # if the name hasn't been changed
            try:  # finding an identically-named course belonging to this user
                Course.objects.filter(user=user).get(name=self.cleaned_data['name'])
            except Course.DoesNotExist:
                return True
            else:
                return False
        return True

    def delete(self):
        """Delete the given course."""
        TimeInterval.objects.filter(course=self.cleaned_data['edit_course']).delete()
        self.cleaned_data['edit_course'].delete()

    def save(self, user, commit):
        """Applies the edits to the selected course."""
        if self.cleaned_data['name']:  # don't change name if not specified
            self.cleaned_data['edit_course'].name = self.cleaned_data['name']
        self.cleaned_data['edit_course'].hours = self.cleaned_data['hours']
        self.cleaned_data['edit_course'].activated = self.cleaned_data['activated']
        if commit:
            self.cleaned_data['edit_course'].save()
        return self.cleaned_data['edit_course']

    class Meta:
        model = Course

        fields = ('name', 'hours', 'activated', )
        exclude = ('user', )  # we don't want to show them all users in the database
