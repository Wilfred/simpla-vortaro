# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (u'^$', 'projektoj.vortaro.views.index'),
    (u'^serĉi$', 'projektoj.vortaro.views.search_word'),
    (u'^vorto/(?P<word>.*)$', 'projektoj.vortaro.views.view_word'),
)
