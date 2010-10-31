from django import template

register = template.Library()

@register.simple_tag
def render_morphemes(morphemes):
    # {{ render_morphemes morphemes }}

    final_string = u""
    is_first = True

    for (i, morpheme) in enumerate(morphemes):
        # the last element
        if i == len(morphemes) - 1:
            if type(morpheme) == str or type(morpheme) == unicode:
                # if stemming produced an ending, the ending is a string
                final_string +=  morpheme
            else:
                # stemming didn't produce an ending, treat as normal
                final_string += u'<a href="?vorto=%s">%s</a>' % \
                    (morpheme.primary_word, morpheme.morpheme)
        else:
            final_string += u'<a href="?vorto=%s">%s</a>-' % \
                (morpheme.primary_word, morpheme.morpheme)

    return final_string
