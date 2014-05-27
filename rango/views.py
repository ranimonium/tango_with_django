from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page


def index(request):
	context = RequestContext(request)

	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}

	# We loop through each category returned, and create a URL attribute.
	# This attribute stores an encoded URL (e.g. spaces replaced with underscores).
	for category in category_list:
		category.url = category.name.replace(' ', '_')

	return render_to_response('rango/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	context_dict = {'boldmessage' : "this the fcking about page"}
	return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):
	# Request our context from the request passed to us.
	context = RequestContext(request)

	# Change underscores in the category name to spaces.
	category_name = category_name_url.replace('_', ' ')

	# Create a context dictionary which we can pass to the template rendering engine.
	context_dict = {'category_name': category_name}

	try:
		category = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass

	return render_to_response('rango/category.html', context_dict, context)