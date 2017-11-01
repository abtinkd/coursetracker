from django import forms
from django.utils import timezone
#from datetimewidget.widgets import DateWidget


class DateRangeForm(forms.Form):
    start_date = forms.DateField(initial=timezone.datetime.today() - timezone.timedelta(weeks=1))
    end_date = forms.DateField(initial=timezone.datetime.today())

    def is_valid(self):  # TODO form error
        """Ensure that the start date is before or equal to the end date (as entered)."""
        if not super().is_valid():
            return False
        # Question - bad practice to change in is_valid?
        self.cleaned_data['end_date'] += timezone.timedelta(days=1)  # show TimeIntervals saved *on* end date
        # Ensure correct format is used
        self.cleaned_data['start_date'] = self.cleaned_data['start_date'].strftime('%m-%d-%Y')
        self.cleaned_data['end_date'] = self.cleaned_data['end_date'].strftime('%m-%d-%Y')
        return self.cleaned_data['end_date'] > self.cleaned_data['start_date']

    # TODO fix
    """class Meta:  
        widgets = {'start_date': DateWidget(usel10n=True, bootstrap_version=3),
                   'end_date': DateWidget(usel10n=True, bootstrap_version=3)}"""
