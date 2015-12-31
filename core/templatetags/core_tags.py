import calendar

from django import template
from django.core.urlresolvers import resolve

register = template.Library()


# usage: {% navactive request 'comma-separated-list,of-url-pattern-names,to-match'}
@register.simple_tag
def navactive(request, urls):
    urls = [url.strip() for url in urls.split(',')]
    current = resolve(request.path)
    if current.url_name in urls or u'{}:{}'.format(current.namespace, current.url_name) in urls:
        return "active"
    return ''


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
