from django import template
from urllib.parse import quote_plus
register = template.Library()

@register.filter
def urlify(url):
    return quote_plus(url)
