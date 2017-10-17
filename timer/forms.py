import datetime
from django import forms
from timer.models import TimeInterval


class TimeIntervalForm(forms.ModelForm):
    start_time = forms.DateTimeField(initial=datetime.datetime.now())

    class Meta:
        model = TimeInterval

        fields = ('course', 'start_time', )
        exclude = ('end_time', )  # we set the times automatically in this implementation
