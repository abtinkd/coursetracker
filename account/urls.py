from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [

	url(r'^$', views.home),
	url(r'^login/$', login, {'template_name': 'account/login.html'}),
	url(r'^logout/$', logout, {'template_name': 'account/logout.html'}),
	url(r'^signup/$', views.signup, name = 'signup'),

]
