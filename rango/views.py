from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def add_category(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)
		print request.POST
		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print form.errors

	else:
		form = CategoryForm()

	return render_to_response('rango/add_category.html', {'form': form}, context)

def register(request):
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':

		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()

			# Update our variable to tell the template registration was successful.
			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'rango/register.html',
		{'user_form':user_form, 'profile_form':profile_form, 'registered':registered},
		context)

def user_login(request):

	context = RequestContext(request)

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:

			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:

			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied")

	else:

		return render_to_response('rango/login.html', {}, context)

@login_required
def restricted(request):
	return HttpResponse("UR LOGED IN")

@login_required
def	user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

