from . import views
from django.conf.urls import url
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login/', login, {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^signup/', views.signup, name='signup')
]
