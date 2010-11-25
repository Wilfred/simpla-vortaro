from django import template

register = template.Library()

@register.simple_tag
def render_morphemes(morphemes):
    # {{ render_morphemes morphemes }}

    final_string = u""
    is_first = True

    return '-'.join([morpheme_to_html(morpheme) for morpheme in morphemes])

def morpheme_to_html(morpheme):
    if type(morpheme) == str or type(morpheme) == unicode:
        # successful stemming produces strings in the parse
        return morpheme

    # morpheme object:
    if morpheme.primary_word:
        # normal case
        return u'<a href="?vorto=%s">%s</a>' % \
            (morpheme.primary_word, morpheme.morpheme)
    else:
        # only occurs on -ant, -int, -ont, -unt
        return morpheme.morpheme
