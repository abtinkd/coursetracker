from timezone_field import TimeZoneFormField
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form


class TimezoneUserCreationForm(UserCreationForm):
    timezone = TimeZoneFormField()  # TODO save to UserProfile


class SettingsForm(Form):
    timezone = TimeZoneFormField()
