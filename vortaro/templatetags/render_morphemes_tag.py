from django import template
from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_morphemes(morphemes):
    # {% render_morphemes morphemes %}
    return mark_safe('-'.join([morpheme_to_html(morpheme) for morpheme in morphemes]))

def morpheme_to_html(morpheme):
    if isinstance(morpheme, str):
        # successful stemming produces strings in the parse
        return conditional_escape(morpheme)

    # morpheme object:
    if morpheme.primary_word:
        # normal case
        return format_html(u'<a href="{}">{}</a>',
                           reverse('view_word', args=[morpheme.primary_word]),
                           morpheme.morpheme)
    else:
        # only occurs on participle affixes and endings
        return conditional_escape(morpheme.morpheme)
