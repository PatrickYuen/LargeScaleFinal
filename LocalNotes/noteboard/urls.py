from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views
from .views import *

app_name = 'noteboard'
urlpatterns = [
	#Search Main Page
    url(r'^$', views.main, name='main'),
	url(r'^search/$', views.search, name='search'),
	
	#Register Post
	url(r'^register/$', views.register, name='register'),
	
	#City Page
	url(r'^cities/(?P<pk>[0-9]+)/$', views.CityView.as_view(), name='CityView'),

	#City error page
    url(r'^error/$', views.error, name='error'),
	
	#All City Page
	url(r'^cities/$', views.CitiesView.as_view(), name='CitiesView'),
	
	#User Page
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='UserView'),
	
	#login
	url(r'^login/$', views.login_view, name='login_view'),
	url(r'^logout/$', views.logout_view, name='logout_view'),
	
	#Post, Delete, Edit View
	url(r'^post/$', views.post, name='post'),

	#Delete, Edit View
	url(r'^delete/(?P<id>[0-9]+)/ $', views.delete, name='delete'),
	url(r'^update/(?P<id>[0-9]+)/ $', views.update, name='update'),


	url('^', include('django.contrib.auth.urls'))
]