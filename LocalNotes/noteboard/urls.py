from django.conf.urls import url

from . import views
from .views import CityView, CitiesView, post

app_name = 'noteboard'
urlpatterns = [
	#Search Main Page
    url(r'^$', views.main, name='main'),
	url(r'^search', views.search, name='search'),
	
	#City Page
	url(r'^cities/(?P<pk>[0-9]+)/$', views.CityView.as_view(), name='CityView'),
	url(r'^cities/(?P<id>[0-9]+)/post/$', views.post, name='post'),
	
	#All City Page
	url(r'^cities/$', views.CitiesView.as_view(), name='CitiesView'),
	
	#User Page
]