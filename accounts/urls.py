from . import views
from django.conf.urls import url
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login/', login, {'template_name': 'accounts/login.html'}),
    url(r'^logout/', logout, {'template_name': 'accounts/logout.html'}),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^signup/', views.signup, name='signup')
]
