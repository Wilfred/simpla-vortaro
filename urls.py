# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (u'^.*$', 'projektoj.vortaro.views.index'),
)
