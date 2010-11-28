# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

if settings.DEBUG:
    # serve static files using Django
    urlpatterns = patterns('',
        (r'^informo$', 'vortaro.views.about'),
        # Django excludes GET arguments from the URL, so just match ""
        (u'^$', 'vortaro.views.index'),
        (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/wilfred/html/projektoj/static'}))
else:
    urlpatterns = patterns('',
        (r'^informo$', 'vortaro.views.about'),
        (u'^$', 'vortaro.views.index'))

