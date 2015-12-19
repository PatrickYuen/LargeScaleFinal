from django.conf.urls import include, url

from . import views
from .views import *

from django.contrib.auth import views as auth_views

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
    # url(r'^error/$', views.error, name='error'),
	#Post Page
	url(r'^post/$', views.post, name='post'),
	
	#All City Page
	url(r'^cities/$', views.CitiesView.as_view(), name='CitiesView'),
	
	#User Page
	# url(r'^users/(?P<user_id>[0-9]+)/$', views.UserView.as_view(), name='UserView'),
	# url(r'^users/(?P<username>[^/]+)/$', views.UserView.as_view(), name='UserView'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='UserView'),
	
	#login
	# url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout_view, name='logout_view'),

	url('^', include('django.contrib.auth.urls'))
	
	#Post View
]

