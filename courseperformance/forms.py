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
            if not time.tzinfo:
                time = time.replace(tzinfo=timezone.get_current_timezone())
            return time.astimezone(timezone.get_current_timezone())
        cleaned_data = super().clean()

        if cleaned_data.get("start_date") and cleaned_data.get("end_date") and cleaned_data.get("course"):
            start_date, end_date = convert(dt.combine(cleaned_data['start_date'], dt.min.time())), \
                                   convert(dt.combine(cleaned_data['end_date'], dt.max.time()))
            creation_time, deactivation_time = convert(cleaned_data['course'].creation_time), \
                                               convert(cleaned_data['course'].deactivation_time)
            if end_date < creation_time:
                raise ValidationError('The course was created on {}.'.format(creation_time))

            if not cleaned_data['course'].activated and start_date > deactivation_time:
                raise ValidationError('The course was deactivated on {}.'.format(deactivation_time))

        return cleaned_data
