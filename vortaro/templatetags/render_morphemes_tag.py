from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def render_morphemes(morphemes):
    # {% render_morphemes morphemes %}
    return '-'.join([morpheme_to_html(morpheme) for morpheme in morphemes])

def morpheme_to_html(morpheme):
    if type(morpheme) == str or type(morpheme) == unicode:
        # successful stemming produces strings in the parse
        return morpheme

    # morpheme object:
    if morpheme.primary_word:
        # normal case
        return u'<a href="%s">%s</a>' % \
            (reverse('view_word', args=[morpheme.primary_word]),
             morpheme.morpheme)
    else:
        # only occurs on participle affixes and endings
        return morpheme.morpheme
