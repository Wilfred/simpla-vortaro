from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'projektoj.vortaro.views.index'),
    (r'^serchi/(?P<word>.*)$', 'projektoj.vortaro.views.search_word'),
    (r'^(?P<word>.*)$', 'projektoj.vortaro.views.view_word'),
)
