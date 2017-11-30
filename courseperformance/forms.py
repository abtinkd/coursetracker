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
        def convert(time):
            return time.astimezone(timezone.get_current_timezone())
        cleaned_data = super().clean()
        if cleaned_data.get("start_date") is not None and cleaned_data.get("end_date") is not None and cleaned_data.get("course") is not None:
            # Period's end_date should be >= the selected course's creation_date
            if convert(dt.combine(self.cleaned_data['end_date'], dt.max.time())) < \
                convert(self.cleaned_data['course'].creation_time):
                raise ValidationError('The course was created on {}.'.format(self.cleaned_data['course'].creation_time))

            # Period's start_date should be <= to the selected course's deactivation_date
            if not self.cleaned_data['course'].activated and \
                    convert(dt.combine(self.cleaned_data['start_date'], dt.min.time())) > \
                            convert(self.cleaned_data['course'].deactivation_time):
                raise ValidationError('The course was deactivated on {}.'.format(self.cleaned_data['course'].deactivation_time))

        return cleaned_data
