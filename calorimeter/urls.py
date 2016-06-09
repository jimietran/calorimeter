from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calorimeter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^calorimeter/', include('calorimeter_site.urls', namespace="calorimeter_site")),
    	url(r'^admin/', include(admin.site.urls)),
	#url(r'', include('social_auth.urls')),
)
