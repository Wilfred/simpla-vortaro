# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

if settings.DEBUG:
    # serve static files using Django
    urlpatterns = patterns('',
        (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/wilfred/html/projektoj/static'}),
        (r'^informo$', 'vortaro.views.about'),
        (u'^.*$', 'vortaro.views.index'),
                           )
else:
    urlpatterns = patterns('',
        (r'^informo$', 'vortaro.views.about'),
        (u'^.*$', 'vortaro.views.index'),)

