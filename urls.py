# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.conf import settings
import os.path

static_files_path = os.path.join(settings.PROJECT_DIR, "static")

urlpatterns = patterns('vortaro.views',
    url(r'^informo$', 'about', name="about"),
    url(r'^vorto/(?P<word>.*)$', 'view_word', name="view_word"),
    url(u'^$', 'index', name="index"))

if settings.DEBUG:
    # Serve static files using Django during development.
    urlpatterns += patterns('',
        (r'^resources/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': static_files_path}))
