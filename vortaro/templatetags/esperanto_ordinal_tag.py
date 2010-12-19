# -*- coding: utf-8 -*-
from django import template
from vortaro.spelling import alphabet

register = template.Library()

@register.simple_tag
def esperanto_ordinal(number):
    # {% esperanto_ordinal 4 %} -> ĉ

    return alphabet[number]
