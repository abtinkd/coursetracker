from django.conf.urls import url
from courseperformance import views

app_name = 'courseperformance'
urlpatterns = [
    #/courseperformance/
    url(r'^$', views.index, name='index'),
    #/courseperformance/display
    url(r'^display', views.display_course_performance, name='display_courseperformance'),

]