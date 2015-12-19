from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.views import generic
# from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm


# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return main(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'noteboard/public.html')

	
def main(request):
	return HttpResponseRedirect(reverse('noteboard:search', args=()))

def search(request):
	context = {'user': ''}
	if request.user.is_authenticated():
		context['user'] = request.user
	
	if request.method == 'POST':
		cities_list = City.objects.filter(name__contains = request.POST.get('keyword'))[:5]
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
      return main(request)
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
		if request.user.is_authenticated():
			context['user'] = request.user
		return context
	
class CityView(generic.DetailView):
	model = City
	template_name = 'noteboard/city.html'
	
	def get_context_data(self, **kwargs):
		context = super(CityView, self).get_context_data(**kwargs)  
		context['city'] = self.object
		context['user'] = ''
		if request.user.is_authenticated():
			context['user'] = request.user
		context['posts_list'] = Post.objects.filter(city = self.object).order_by('-created')[:5]
		return context

def post(request):
	current_city = City.objects.get(pk = '1')
	if request.method == 'POST':
		selected_post = Post(
						title = request.POST.get('title'),
						body = request.POST.get('body'),
						city = current_city,
						user = request.user)
		selected_post.save()
		
	return HttpResponseRedirect(reverse('noteboard:CityView', args=(current_city.pk,)))
	
class UserView(generic.DetailView):
	model = User
	template_name = 'noteboard/user.html'
	
	def get_context_data(self, **kwargs):
		context = super(UserView, self).get_context_data(**kwargs)  
		context['user'] = self.object
		context['posts_list'] = Post.objects.filter(user = self.object).order_by('-created')[:5]
		return context
		



# def login(request):
#     m = User.objects.get(username=request.POST['username'])
#     if m.password == request.POST['password']:
#         request.session['member_id'] = m.id
#         return HttpResponseRedirect(reverse('noteboard:UserView', args=(m.id,)))
#     else:
#         return HttpResponse("Your username and password didn't match.")
		
# def logout(request):
#     try:
#         del request.session['member_id']
#     except KeyError:
#         pass
#     return HttpResponseRedirect(reverse('noteboard:search', args=()))