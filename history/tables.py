import django_tables2 as tables
from timer.models import TimeInterval


class TimeIntervalTable(tables.Table):
    class Meta:
        model = TimeInterval

        attrs = {'class': 'paleblue'}
        exclude = ['id', 'course', ]
