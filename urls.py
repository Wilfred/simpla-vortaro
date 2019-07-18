# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView

import vortaro.views as v
import api.views as api

urlpatterns = [
    url(r'^informo$', v.about, name="about"),
    url(r'^informo/api$', v.about_the_api, name="about_the_api"),
    url(ur'^serĉo$', v.search_word, name="search_word"),
    url(r'^vorto/(?P<word>.*)$', v.view_word, name="view_word"),
    url(u'^$', v.index, name="index"),

    url(u'^api/v1/vorto/(?P<word>.+)$', api.view_word, name="api_view_word"),
    # We're deliberately using a non-UTF8 URL prefix to hopefully make it easier
    # to use the API.
    url(u'^api/v1/trovi/(?P<search_term>.+)$', api.search_word, name="api_search_word"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404$', TemplateView.as_view(template_name='404.html')),
        url(r'^500$', TemplateView.as_view(template_name='500.html')),
    ]
