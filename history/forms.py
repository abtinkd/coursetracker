from django import forms
from django.forms import ValidationError
from datetimewidget.widgets import DateWidget


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    # TODO dynamic min date https://stackoverflow.com/questions/40210999/how-to-disable-past-dates-in-bootstrap-datetimepicker-after-set-check-in-date

    def clean_end_date(self):
        if not self.cleaned_data['end_date'] >= self.cleaned_data['start_date']:
            raise ValidationError('The end date must be on or after the start date.')
        return self.cleaned_data['end_date']
