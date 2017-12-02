import django_tables2 as tables


class TimeIntervalTable(tables.Table):
    start_time = tables.Column()
    length = tables.Column()

    class Meta:
        attrs = {'class': 'paleblue'}
        exclude = ['id', 'course', ]
