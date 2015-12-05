from django.shortcuts import render

from .models import *

def main(request):
	if request.method == 'POST':
		form = Post(request.POST)
		form.save()
		return HttpResponseRedirect('/thanks/')

	post_list = Post.objects.order_by('created')[:5]
	context = {'post_list': post_list, 'post': post_list }
	return render(request, 'noteboard/index.html', context)