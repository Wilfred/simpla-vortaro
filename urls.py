# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.conf import settings
import os.path

static_files_path = os.path.join(settings.PROJECT_DIR, "static")

urlpatterns = patterns('vortaro.views',
    url(r'^informo$', 'about', name="about"),
    url(ur'^serĉo$', 'search_word', name="search_word"),
    url(r'^vorto/(?P<word>.*)$', 'view_word', name="view_word"),
    url(u'^$', 'index', name="index"),
)

urlpatterns += patterns('api.views',
    url(u'^api/v1/vorto/(?P<word>.+)$', 'view_word', name="api_view_word"),
    # We're deliberately using a non-UTF8 URL prefix to hopefully make it easier
    # to use the API.
    url(u'^api/v1/trovi/(?P<search_term>.+)$', 'search_word', name="api_search_word"),
)

if settings.DEBUG:
    # Serve static files using Django during development.
    urlpatterns += patterns('',
        (r'^resources/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': static_files_path}))
