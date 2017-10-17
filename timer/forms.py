from django import forms
from django.utils import timezone
from timer.models import TimeInterval


class TimeIntervalForm(forms.ModelForm):
    start_time = forms.DateTimeField(initial=timezone.now())

    class Meta:
        model = TimeInterval

        fields = ('course', 'start_time', )
        exclude = ('end_time', )  # we set the times automatically in this implementation
