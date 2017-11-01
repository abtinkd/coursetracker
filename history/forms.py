import datetime
from django import forms
from datetimewidget.widgets import DateWidget


class HistoryForm(forms.Form):
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3,
                                                   options={'endDate': datetime.date.today, 'startView': 1}))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3,
                                                 options={'endDate': datetime.date.today, 'startView': 1}))

    def is_valid(self):
        """Ensure that the start date is before or equal to the end date."""
        return super().is_valid() and self.start_date <= self.end_date
