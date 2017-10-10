from courses import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_course/$', views.add_course, name='add_course')
]
