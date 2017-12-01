from django.conf.urls import url
from courseperformance import views

app_name = 'courseperformance'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^display', views.display, name='display'),

]