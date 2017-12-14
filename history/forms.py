from courses.models import Course
from datetimewidget.widgets import DateWidget
from django import forms
from django.forms import ValidationError
from django.utils import timezone


class HistoryForm(forms.Form):
    start_date = forms.DateField(widget=DateWidget(usel10n=True, options={'clearBtn': False, 'todayHighlight': True}),
                                 initial=timezone.datetime.today() - timezone.timedelta(weeks=1))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, options={'clearBtn': False, 'todayHighlight': True}),
                               initial=timezone.datetime.today())
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False, label="Course (optional)")
    # TODO dynamic min date https://stackoverflow.com/questions/40210999/how-to-disable-past-dates-in-bootstrap-datetimepicker-after-set-check-in-date
    # https://eonasdan.github.io/bootstrap-datetimepicker/

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
