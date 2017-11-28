from django import forms
from django.forms import ValidationError
from django.utils import timezone
from courses.models import Course



class CourseDateRangeForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")
    start_date = forms.DateField(initial=timezone.datetime.today() - timezone.timedelta(weeks=1))
    end_date = forms.DateField(initial=timezone.datetime.today())


    def clean_end_date(self):
        if not self.cleaned_data['end_date'] >= self.cleaned_data['start_date']:
            raise ValidationError('The end date must be on or after the start date.')
        return self.cleaned_data['end_date']

    def is_valid(self):
        """Ensure that the start date is before or equal to the end date (as entered)."""
        if not super().is_valid():
            return False
        self.cleaned_data['end_date'] += timezone.timedelta(days=1)  # show TimeIntervals saved *on* end date
        # Ensure correct format is used
        self.cleaned_data['start_date'] = self.cleaned_data['start_date'].strftime('%m-%d-%Y')
        self.cleaned_data['end_date'] = self.cleaned_data['end_date'].strftime('%m-%d-%Y')
        return True

    # TODO use widget
    """class Meta:  
        widgets = {'start_date': DateWidget(usel10n=True, bootstrap_version=3),
                   'end_date': DateWidget(usel10n=True, bootstrap_version=3)}"""
