from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.gis.geoip2 import GeoIP2
# from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm

from .models import *
from .hints import * 
from .routers import LOGICAL_TO_PHYSICAL, logical_to_physical, logical_shard_for_city

global geo
geo = GeoIP2()

def main(request):
	return HttpResponseRedirect(reverse('noteboard:search', args=()))

def search(request):
	context = {'user': None}
	if request.user.is_authenticated():
		context['user'] = request.user

	if request.method == 'POST':
		#go through the default cities DB
		cities_list = City.objects.filter(name__icontains = request.POST.get('keyword').strip())[:5]
		context = {'cities_list': cities_list}	

	return render(request, 'noteboard/search.html', context)

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save(commit=True)
      # Log in that user.
      user = authenticate(username=new_user.username,
                          password=form.clean_password2())
      if user is not None:
        login(request, user)
      else:
        raise Exception
      return HttpResponseRedirect(reverse('noteboard:UserView', args=(user.id,)))
  else:
    form = UserCreationForm
  return render(request, 'noteboard/register.html', {'form' : form})


class CitiesView(generic.ListView):
	template_name = 'noteboard/cities.html'
	context_object_name = 'cities_list'

	def get_queryset(self):
		return City.objects.order_by('name') #defaulted to cities table
		
	def get_context_data(self, **kwargs):
		context = super(CitiesView, self).get_context_data(**kwargs)  
		context['user'] = ''
		if self.request.user.is_authenticated():
			context['user'] = self.request.user
		return context
	
class CityView(generic.DetailView):
	model = City
	template_name = 'noteboard/city.html'
	
	def get_context_data(self, **kwargs):
		context = super(CityView, self).get_context_data(**kwargs)  
		context['city'] = self.object
		context['user'] = ''
		if self.request.user.is_authenticated():
			context['user'] = self.request.user
		context['posts_list'] = Post.objects.filter(city = self.object).order_by('-created')[:5]
		set_city_for_sharding(context['posts_list'], self.object.id) #go to corresponding shard (City's PK = the corresponding shard)
		
		return context

def post(request):

	ip_address = '216.165.95.3'
	#request.META.get('REMOTE_ADDR')

	current_city = geo.city(str(ip_address))
	city_name = str(current_city['city'])
	country_name = str(current_city['country_name'])
	
	user_city = ""

	input_city_country = request.POST.get('city')

	if input_city_country == "":

		try:
			user_city = City.objects.get(name=city_name)

		except City.DoesNotExist:
			user_city = City(name=city_name, country=country_name, summary="Please add summary")
			user_city.save(using='cities') #update cities DB
			print user_city.id
			user_city.save(using=logical_to_physical(logical_shard_for_city(user_city.id)),force_insert=True) 
			#update corresponding shard: Important they have the same PID

		input_city = city_name
		input_country = country_name

	else:
		user_city = City.objects.get(using='cities', name=city_name) # Get PK from Cities
		user_city = City.objects.get(using=logical_to_physical(logical_shard_for_city(user_city.id)), name=city_name) 
		#Find City Obj in Corresponding Shard
		input_city = str(input_city_country.split("+")[0])
		input_country = str(input_city_country.split("+")[1])

	#get user
	
	if input_city == city_name and country_name == input_country:
		if request.method == 'POST' and user_city != "":

			selected_post = Post(
							title = request.POST.get('title'),
							body = request.POST.get('body'),
							city = user_city,
							userid = request.user.id,
							user = request.user.username
							)
			selected_post.save(using=logical_to_physical(logical_shard_for_city(user_city.id)),force_insert=True)

		return HttpResponseRedirect(reverse('noteboard:CityView', args=(user_city.pk,)))

	else:
		return error(request, "The city selected does not match the current city you are in, please re-add post.")

def error(request, err_message):
    context = dict()
    context['messages'] = err_message

    context['user'] = request.user
    return render(request, 'noteboard/city_error.html', context)

class UserView(generic.DetailView):
	model = User
	template_name = 'noteboard/user.html'
	
	def get_context_data(self, **kwargs):
		context = super(UserView, self).get_context_data(**kwargs)  
		context['user'] = self.object
		# Fan in for all posts
		allposts = []
		for db in set(LOGICAL_TO_PHYSICAL):
			print db
			posts = Post.objects.filter(userid = self.object.id).order_by('-created')[:5]
			set_shard(posts, db)
			allposts = allposts + [p for p in posts]	
			
		context['posts_list'] = allposts
		return context

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,
                        password=password)

    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse('noteboard:UserView', args=(user.id,)))
    else:
      # return render_to_response('login_error', message='Save complete')
      return HttpResponse("Your username and password didn't match.")
    
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('noteboard:search', args=()))