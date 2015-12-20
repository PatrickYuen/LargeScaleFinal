from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.gis.geoip2 import GeoIP2
# from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm

from .models import *

global geo
geo = GeoIP2()

def main(request):
	return HttpResponseRedirect(reverse('noteboard:search', args=()))

def search(request):
	context = {'user': None}
	if request.user.is_authenticated():
		context['user'] = request.user

	if request.method == 'POST':
		cities_list = City.objects.filter(name__contains = request.POST.get('keyword'))[:5]

		context = {'cities_list': cities_list}		

	return render(request, 'noteboard/search.html', context)

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('noteboard:UserView', args=(request.user.id,)))

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
		return City.objects.order_by('name')[:5]
		
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
		return context

@login_required
def post(request):

		ip_address = request.META.get('REMOTE_ADDR')

		current_city = geo.city(str(ip_address))
		city_name = str(current_city['city'])
		country_name = str(current_city['country_name'])
		print city_name

		input_city_country = request.POST.get('city')

		if input_city_country == "":

				try:
						City.objects.get(name=city_name)

				except City.DoesNotExist:
						user_city = City(name=city_name, country=country_name, summary="Please add summary")
						user_city.save()

				input_city = city_name
				input_country = country_name

		else:
				input_city = str(input_city_country.split("+")[0])
				input_country = str(input_city_country.split("+")[1])

		if input_city == city_name and country_name == input_country:
				user_city = City.objects.get(name=city_name)
				if request.method == 'POST':

						selected_post = Post(
														title = request.POST.get('title'),
														body = request.POST.get('body'),
														city = user_city,
														user = request.user)

						selected_post.save()

				return HttpResponseRedirect(reverse('noteboard:CityView', args=(user_city.pk,)))

		else:
				return error(request, "The city selected does not match the current city you are in, please re-add post.")

@login_required
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
		context['user'] = self.request.user
		context['posts_list'] = Post.objects.filter(user = self.object).order_by('-created')[:5]
		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(UserView, self).dispatch(*args, **kwargs)


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

@login_required	
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('noteboard:search', args=()))