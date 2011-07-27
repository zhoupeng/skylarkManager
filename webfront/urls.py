from django.conf.urls.defaults import patterns, include, url
import vApp.urls
import vApp.views
import accounts.account

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webfront.views.home', name='home'),
    # url(r'^webfront/', include('webfront.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # testing through web
     url(r'^webtester$', 'django.views.generic.simple.direct_to_template', {'template': 'webtester.html'}),
     url(r'^ajax_tester$', 'django.views.generic.simple.direct_to_template', {'template': 'ajax_tester.html'}),

     url(r'^api/vapp$', vApp.views.api_vapp),
     url(r'^api/accounts$', accounts.account.api_account),
)
