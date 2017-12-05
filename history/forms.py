from courses.models import Course
from django import forms
from django.forms import ValidationError
from datetimewidget.widgets import DateWidget


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False,
                                    label="Course-specific performance (optional)")  # TODO test
    # TODO dynamic min date https://stackoverflow.com/questions/40210999/how-to-disable-past-dates-in-bootstrap-datetimepicker-after-set-check-in-date

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=self.user).order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("start_date") is not None and cleaned_data.get("end_date") is not None:
            if not self.cleaned_data['end_date'] >= self.cleaned_data['start_date']:
                raise ValidationError('The end date must be on or after the start date.')
        return cleaned_data
