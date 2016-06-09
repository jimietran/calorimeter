from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse

from calorimeter_site import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^index/$', views.index, name='index'),
	url(r'^auth/$', views.auth_view, name='auth_view'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^loggedin/$', views.loggedin, name='loggedin'),
	url(r'^invalid/$', views.invalid, name='invalid'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register_success/$', views.register_success, name='register_success'),
	url(r'^meal_plan_search/$', views.meal_plan_search, name='meal_plan_search'),
	url(r'^meal_plan_detail/$', views.meal_plan_detail, name='meal_plan_detail'),
	url(r'^nutrition/$', views.nutrition, name='nutrition'),
	url(r'^grocery_store_locator/$', views.grocery_store_locator, name='grocery_store_locator'),
	url(r'^alreadyloggedin/$', views.alreadyloggedin, name='alreadyloggedin'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^editprofile/$', views.editprofile, name='editprofile'),
	url(r'^about/$', views.about, name='about'),
	url(r'^food_search/$', views.food_search, name='food_search'),
	url(r'^food_list/$', views.food_list, name='food_list'),
	url(r'^food_detail/$', views.food_detail, name='food_detail'),
	url(r'^password_change/$', views.password_change, name='password_change'),
	url(r'^password_change_done/?', views.password_change_done, name='password_change_done'),
)
