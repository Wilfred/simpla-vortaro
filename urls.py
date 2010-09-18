from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'projektoj.vortaro.views.index'),
    (r'^serchi/(?P<word>[a-zA-Z]*)$', 'projektoj.vortaro.views.search_word'),
    (r'^(?P<word>[a-zA-Z]+)$', 'projektoj.vortaro.views.view_word'),
    # Example:
    # (r'^projektoj/', include('projektoj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
