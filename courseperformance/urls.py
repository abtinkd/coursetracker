from django.conf.urls import url
from courseperformance import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^display', views.display_courseperformance, name='display'),
]