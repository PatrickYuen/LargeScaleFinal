from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Post, City
	
def main(request):
	return HttpResponseRedirect(reverse('noteboard:search', args=()))

def search(request):
	context = {}
	
	if request.method == 'POST':
		cities_list = City.objects.filter(name__contains = request.POST.get('keyword'))[:5]
		context = {'cities_list': cities_list}
		
	return render(request, 'noteboard/search.html', context)

class CitiesView(generic.ListView):
	template_name = 'noteboard/cities.html'
	context_object_name = 'cities_list'

	def get_queryset(self):
		return City.objects.order_by('name')[:5]
		
def cities(request):
	cities_list = City.objects.order_by('name')[:10]
	context = {'cities_list': cities_list}
	return render(request, 'noteboard/cities.html', context)
	
class CityView(generic.DetailView):
	model = City
	template_name = 'noteboard/city.html'
	
	def get_context_data(self, **kwargs):
		context = super(CityView, self).get_context_data(**kwargs)  
		context['city'] = self.object
		context['posts_list'] = Post.objects.filter(city = self.object).order_by('-created')[:5]
		return context

def post(request, id):
	current_city = City.objects.get(pk = id)
	if request.method == 'POST':
		selected_post = Post(
						title = request.POST.get('title'),
						body = request.POST.get('body'),
						city = current_city )
		selected_post.save()
		
	return HttpResponseRedirect(reverse('noteboard:CityView', args=(id)))