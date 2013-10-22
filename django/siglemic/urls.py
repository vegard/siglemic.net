from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from website.views import site_login, site_logout, site_authenticate, site_main

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siglemic.views.home', name='home'),
    # url(r'^siglemic/', include('siglemic.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^login/?$', site_login),
    url(r'^logout/?$', site_logout),
    url(r'^authenticate/?$', site_authenticate),

    url(r'^/?$', site_main),
)
