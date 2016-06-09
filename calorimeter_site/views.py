# Import statements #
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib import auth
from calorimeter_site.forms import UserForm, UserProfileForm, ChangePasswordForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from calorimeter_site.models import UserProfile, Food
from pprint import pprint
from django.contrib.auth.views import password_change
from django.contrib.auth import authenticate

from fatsecret import FatSecretClient, FatSecretApplication
from fatsecret import FatSecretError

import json

# Initialize Fatsecret API
class FatSecretTestApplication(FatSecretApplication):
	key = "1ff75681e8c44a8eb3f808654bf7a4e1"
	secret = "9c62fcd28e01496083383a45cf33882a"

#client = FatSecretClient().connect().setApplication(FatSecretTestApplication)

# Home page
def index(request):
	return render(request, 'calorimeter_site/index.html')

# Login page
def login(request):
	# Redirect user if user is already logged in
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('calorimeter_site:alreadyloggedin'), request)
	else:
		return render(request, 'calorimeter_site/login.html')

# Authentication for login
def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect(reverse('calorimeter_site:loggedin'))
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:invalid'))

# Login success page
def loggedin(request):
	return render(request, 'calorimeter_site/loggedin.html')

# Invalid username/password page
def invalid(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('calorimeter_site:alreadyloggedin'), request)
	else:
		return render(request, 'calorimeter_site/invalid.html')

# Logout confirmation page
def logout(request):
	auth.logout(request)
	return render(request, 'calorimeter_site/logout.html')

# User registration page
def register(request):
	# Redirect user if user already logged in
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('calorimeter_site:alreadyloggedin'), request)
			
	if request.method == 'POST':
		userform = UserForm(data=request.POST)
		userprofileform = UserProfileForm(data=request.POST)
		
		if userform.is_valid() and userprofileform.is_valid():
			user = userform.save()
			user.set_password(user.password)
			user.save()

			userprofile = userprofileform.save(commit=False)
			userprofile.user = user
			userprofile.save()

			return HttpResponseRedirect(reverse('calorimeter_site:register_success'))

		else:
			print userform.errors, userprofileform.errors

	else:
		userform = UserForm()
		userprofileform = UserProfileForm()

	args = {}
	args['userform'] = userform
	args['userprofileform'] = userprofileform
	
	return render(request, 'calorimeter_site/register.html', args)

# Registration success page
def register_success(request):
	# Redirect user if user already logged in
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('calorimeter_site:alreadyloggedin'), request)
	else:
		return render(request, 'calorimeter_site/register_success.html')

#####################################################################################

# Meal plan page
def meal_plan_search(request):
	# Only allow users who are logged in to access the page
	if request.user.is_authenticated():
		return render(request, 'calorimeter_site/meal_plan_search.html')
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

def meal_plan_detail(request):
	mealquery = request.GET['mealquery']
	result_num = request.GET['max_results']
	meal_type = request.GET['meal_types']

	if mealquery is u'':
		return render(request, 
						'calorimeter_site/meal_plan_search.html', 
						{'error_message' : "Please enter a search term!"})

	if result_num is "":
		result_num = 10

	if request.user.is_authenticated():
		client = FatSecretClient().connect().setApplication(FatSecretTestApplication)
		try:
			data=client.recipes.search(search_expression=mealquery, 
										max_results=result_num, 
										recipe_type=meal_type)
		except:
			return render(request, 
						'calorimeter_site/meal_plan_search.html', 
						{'error_message' : "API is down, please try again later."})

		result_size = int(data['recipes']['max_results'])
		total_results = int(data['recipes']['total_results'])

		if u'recipes' in data:
			if total_results is 0:
				return render(request, 
						'calorimeter_site/meal_plan_search.html', 
						{'error_message' : "Meal not found!"})
			if result_size is 1:
				recipe_data = client.recipe.get(recipe_id=data['recipes']['recipe']['recipe_id'])
				#with open('meal_data.json', 'w') as outfile:
				#	json.dump(recipe_data, outfile)
				return render(request,
						'calorimeter_site/meal_plan_detail_single.html',
						{'meals' : recipe_data})
			else:
				return render(request, 
						'calorimeter_site/meal_plan_detail_multiple.html', 
						{'meals' : data, 'mealquery' : mealquery})
		else:
			return render(request, 
						'calorimeter_site/meal_plan_search.html', 
						{'error_message' : "Meal not found!"})
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

#####################################################################################

# Exercise plan page
def nutrition(request):
	# Only allow users who are logged in to access the page
	if request.user.is_authenticated():
		return render(request, 'calorimeter_site/nutrition.html')
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

def grocery_store_locator(request):
	# Only allow users who are logged in to access the page
	if request.user.is_authenticated():
		return render(request, 'calorimeter_site/grocery_store_locator.html')
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)
		
# User is already logged in page
def alreadyloggedin(request):
	if request.user.is_authenticated():
		return render(request, 'calorimeter_site/alreadyloggedin.html')
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

# User profile page
def profile(request):
	try:
		extraprofileinfo = UserProfile.objects.get(user=request.user)
	except:
		extraprofileinfo = None
	
	args = {}
	args['extraprofileinfo'] = extraprofileinfo

	if request.user.is_authenticated():
		return render(request, 'calorimeter_site/profile.html', args)
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

# Edit profile page
def editprofile(request):
	user=request.user
	user_profile = user.get_profile()
	if request.user.is_authenticated():
		try:
			extraprofileinfo = UserProfile.objects.get(user=request.user)
		except:
			extraprofileinfo = None	

		args = {}
		args['extraprofileinfo'] = extraprofileinfo

		if request.method == 'POST':

			userprofileform = UserProfileForm(data=request.POST, instance=user_profile)

			if userprofileform.is_valid():
				userprofileform.save()
				return HttpResponseRedirect(reverse('calorimeter_site:profile'))

			else:
				print userprofileform.errors

		else:
			userprofileform = UserProfileForm(initial={
										 'first_name':extraprofileinfo.first_name,
										 'last_name':extraprofileinfo.last_name, 
										 'email':extraprofileinfo.email,
										 'age':extraprofileinfo.age, 
										 'gender':extraprofileinfo.gender,
										 'weight':extraprofileinfo.weight, 
										 'height':extraprofileinfo.height,
										})

		args = {}
		args['userprofileform'] = userprofileform
	
		return render(request, 'calorimeter_site/editprofile.html', args)
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

# Password changing page
def password_change(request):
	if request.user.is_authenticated():
		user = request.user
		try:
			extraprofileinfo = UserProfile.objects.get(user=request.user)
		except:
			extraprofileinfo = None	

		args = {}
		args['extraprofileinfo'] = extraprofileinfo
		
		if request.method == 'POST':
			passwordchangeform = ChangePasswordForm(request.POST)

			if passwordchangeform.is_valid():
				new_password = passwordchangeform.cleaned_data['newpassword1']

				user.set_password(new_password)
				user.save()
				return HttpResponseRedirect(reverse('calorimeter_site:password_change_done'))

			else:
				print passwordchangeform.errors

		else:
			passwordchangeform = ChangePasswordForm()

		args['passwordchangeform'] = passwordchangeform

		return render(request, 'calorimeter_site/password_change.html', args)
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

def password_change_done(request):
	return render(request, 'calorimeter_site/password_change_done.html')

# About us page
def about(request):
	return render(request, 'calorimeter_site/about.html')

# Food search
def food_search(request):
	if request.user.is_authenticated():
		return render(request, 'calorimeter_site/food_search.html')
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

def food_list(request):
	data = {}
	searchquery = request.GET['searchquery']

	if request.user.is_authenticated():
		client = FatSecretClient().connect().setApplication(FatSecretTestApplication)
		try:
			data=client.foods.search(search_expression=searchquery, 
									max_results=1)
		except:
			return render(request, 
						'calorimeter_site/food_search.html', 
						{'error_message' : "API is down, please try again later."})

		if u'foods' in data:
			try:
				food_id = data['foods']['food']['food_id']
			except:
				return render(request, 
						'calorimeter_site/food_search.html', 
						{'error_message' : "Food not found!"})

			food_data = client.food.get(food_id = food_id)

			# Count how many instances of servings are returned. Actions vary depending on count.
			count = 0
			for serving_description in food_data['food']['servings']['serving']:
				if u'serving_description' in serving_description:
					count = count + 1
					pprint(serving_description)

			if count is 1:
				return food_detail(request, food_data)
			else:
				return show_food_list(request, food_data)
				#return render(request, 'calorimeter_site/food_list.html', {'object_list': food_data})
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)

# Deal with multiple serving sizes being returned, show a list to user.
def show_food_list(request, data):
	food_data = data
	if request.user.is_authenticated():
		return render(request, 
					'calorimeter_site/food_detail_multiple.html', 
					{'object_list' : food_data})
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)
	
# Show details of one serving
def food_detail(request, data):
	food_data = data
	if request.user.is_authenticated():
		return render(request, 
					'calorimeter_site/food_detail.html', 
					{'object_list' : food_data})
	else:
		return HttpResponseRedirect(reverse('calorimeter_site:login'), request)
