import calendar
import re

from django import template
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

import markdown as mkdn


register = template.Library()


# usage: {% navactive request 'comma-separated-list,of-url-pattern-names,to-match' %}
@register.simple_tag
def navactive(request, urls):
    urls = [url.strip() for url in urls.split(',')]
    current = resolve(request.path)
    if current.url_name in urls or u'{}:{}'.format(current.namespace, current.url_name) in urls:
        return "active"
    return ''


# usage: {% current_site %}
@register.simple_tag
def current_domain():
    site = Site.objects.first()
    return site.domain


@register.filter(name='month_name')
def month_name(value):
    """
    Converts month number to name
    """
    try:
        month_num = int(value)
    except ValueError:
        return value
    name = calendar.month_name[month_num]
    if name:
        return name
    else:
        return value


@register.filter(name='day_name')
def day_name(value):
    """
    Converts day number to name
    """
    try:
        month_num = int(value)
    except ValueError:
        return value
    name = calendar.day_name[month_num]
    if name:
        return name
    else:
        return value


@register.filter(name='get_range')
def get_range(value):
    """
    Returns range(value)
    """
    try:
        value = int(value)
        return range(value)
    except:
        return value


# usage: {% render_error error_text[|escape] %}
@register.simple_tag
def render_error(error_text):
    return u'<div class="alert alert-danger">{0}</div>'.format(error_text)


@register.simple_tag
def dump(obj):
    return repr(obj)


@register.filter()
def markdown(value):
    return mark_safe(mkdn.markdown(value, safe_mode='escape'))


CONSONANT_SOUND = re.compile(r'''
one(![ir])
''', re.IGNORECASE|re.VERBOSE)
VOWEL_SOUND = re.compile(r'''
[aeio]|
u([aeiou]|[^n][^aeiou]|ni[^dmnl]|nil[^l])|
h(ier|onest|onou?r|ors\b|our(!i))|
[fhlmnrsx]\b
''', re.IGNORECASE|re.VERBOSE)


@register.filter
@stringfilter
def an(text):
    """
    Guess "a" vs "an" based on the phonetic value of the text.

    "An" is used for the following words / derivatives with an unsounded "h":
    heir, honest, hono[u]r, hors (d'oeuvre), hour

    "An" is used for single consonant letters which start with a vowel sound.

    "A" is used for appropriate words starting with "one".

    An attempt is made to guess whether "u" makes the same sound as "y" in
    "you".
    """
    text = force_unicode(text)
    if not CONSONANT_SOUND.match(text) and VOWEL_SOUND.match(text):
        return 'an'
    return 'a'
