"""
From: http://djangosnippets.org/snippets/17/

"Widows" are single words that end up on their own line, thanks to automatic line-breaks. This is an no-no in graphic design, and is especially unsightly in headers and other short bursts of text. This filter automatically replaces the space before the last word of the passed value with a non-breaking space, ensuring there is always at least two words on any given line. Usage is like so:

{{ blog.entry.headline|widont }}
"""
from django.template import Library, Node


register = Library()


def widont(value):
    bits = value.rsplit(' ', 1)
    try:
        widowless = bits[0] + "&nbsp;" + bits[1]
        return widowless
    except:
        return value
register.filter(widont)