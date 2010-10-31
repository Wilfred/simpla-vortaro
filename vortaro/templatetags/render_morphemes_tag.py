from django import template

register = template.Library()

@register.simple_tag
def render_morphemes(morphemes):
    # {{ render_morphemes morphemes }}

    final_string = u""
    is_first = True

    for (i, morpheme) in enumerate(morphemes):
        # we don't link the list element, which is just a string
        if i == len(morphemes) - 1:
            final_string +=  morpheme
        else:
            final_string += u'<a href="?vorto=%s">%s</a>-' % \
                (morpheme.primary_word, morpheme.morpheme)

    return final_string
