import django_tables2 as tables
from courses.models import Course


class CourseTable(tables.Table):
    class Meta:
        model = Course

        attrs = {'class': 'paleblue'}
        exclude = ['id', 'user', 'deactivation_datetime', ]
