# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.conf import settings
import os.path

static_files_path = os.path.join(settings.PROJECT_DIR, "static")

if settings.DEBUG:
    # serve static files using Django
    urlpatterns = patterns('',
        (r'^informo$', 'vortaro.views.about'),
        # Django excludes GET arguments from the URL, so just match ""
        (u'^$', 'vortaro.views.index'),
        (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static_files_path}))
else:
    urlpatterns = patterns('',
        (r'^informo$', 'vortaro.views.about'),
        (u'^$', 'vortaro.views.index'))

