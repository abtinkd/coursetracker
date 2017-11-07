from django import forms
from courses.models import Course


class CourseSelectionForm(forms.Form):  # TODO test
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user, activated=True).order_by('name')

    class Meta:
        fields = ('course', )
