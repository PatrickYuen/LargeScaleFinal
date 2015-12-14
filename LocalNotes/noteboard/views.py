from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.gis.geoip2 import GeoIP2

from .models import *
	
def main(request):
	return HttpResponseRedirect(reverse('noteboard:search', args=()))

def search(request):
	context = {'user': ''}
	if 'member_id' in request.session:
		context['user'] = User.objects.get(id = request.session['member_id'])
	
	if request.method == 'POST':
		cities_list = City.objects.filter(name__contains = request.POST.get('keyword'))[:5]
		context = {'cities_list': cities_list}
			
	return render(request, 'noteboard/search.html', context)

class CitiesView(generic.ListView):
	template_name = 'noteboard/cities.html'
	context_object_name = 'cities_list'

	def get_queryset(self):
		return City.objects.order_by('name')[:5]
		
	def get_context_data(self, **kwargs):
		context = super(CitiesView, self).get_context_data(**kwargs)  
		context['user'] = ''
		if 'member_id' in self.request.session:
			context['user'] = User.objects.get(id = self.request.session['member_id'])
		return context
	
class CityView(generic.DetailView):
	model = City
	template_name = 'noteboard/city.html'
	
	def get_context_data(self, **kwargs):
		context = super(CityView, self).get_context_data(**kwargs)  
		context['city'] = self.object
		context['user'] = ''
		if 'member_id' in self.request.session:
			context['user'] = User.objects.get(id = self.request.session['member_id'])
		context['posts_list'] = Post.objects.filter(city = self.object).order_by('-created')[:5]
		return context

def post(request):
	host = request.META.get('REMOTE_HOST')
	ip_address = request.META.get('REMOTE_ADDR')

	geo = GeoIP2()
	current_city = geo.city(str(ip_address))
	city_name = str(current_city['city'])
	country_name = str(current_city['country_name'])

	if len(City.objects.filter(name=city_name)) == 0:
		user_city = City(name=city_name, country=country_name, summary="Please add summary")
		user_city.save()
	else:
		user_city = City.objects.get(name=city_name)
	if request.method == 'POST':
		selected_post = Post(
						title = request.POST.get('title'),
						body = request.POST.get('body'),
						city = user_city,
						user = User.objects.get(id = request.session['member_id']))
		selected_post.save()
		
	return HttpResponseRedirect(reverse('noteboard:CityView', args=(user_city.pk,)))
	
class UserView(generic.DetailView):
	model = User
	template_name = 'noteboard/user.html'
	
	def get_context_data(self, **kwargs):
		context = super(UserView, self).get_context_data(**kwargs)  
		context['user'] = self.object
		context['posts_list'] = Post.objects.filter(user = self.object).order_by('-created')[:5]
		return context
		
def register(request):
	if request.method == 'POST':
		selected_user = User(
						username = request.POST.get('username'),
						password = request.POST.get('password'),
						 )
		selected_user.save()
		return HttpResponseRedirect(reverse('noteboard:UserView', args=(selected_user.id,)))
		
	return HttpResponseRedirect(reverse('noteboard:search', args=()))
	
def login(request):
    m = User.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponseRedirect(reverse('noteboard:UserView', args=(m.id,)))
    else:
        return HttpResponse("Your username and password didn't match.")
		
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('noteboard:search', args=()))
