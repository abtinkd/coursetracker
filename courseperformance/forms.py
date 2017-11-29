from courses.models import Course
from datetime import datetime as dt
from django import forms
from django.forms import ValidationError
from django.utils import timezone
from history.forms import DateRangeForm


class CourseDateRangeForm(DateRangeForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=self.user).order_by('name')

    def clean(self):
        # Period's end_date should be >= the selected course's creation_date
        if dt.combine(self.cleaned_data['end_date'], dt.max.time()) < \
            self.cleaned_data['course'].creation_time.astimezone(timezone.get_current_timezone()):
            raise ValidationError('The course was created on {}.'.format(self.cleaned_data['course'].creation_time))

        # Period's start_date should be <= to the selected course's deactivation_date
        if not self.cleaned_data['course'].activated and \
                self.cleaned_data['start_date'] > \
                self.cleaned_data['course'].deactivation_time.astimezone(timezone.get_current_timezone()):
            raise ValidationError('The course was deactivated on {}.'.format(self.cleaned_data['course'].deactivation_time))

        return super().clean()
