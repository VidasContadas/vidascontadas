from django import template

register = template.Library()

@register.filter(name='url_open')
def url_open(text):
    if not "target" in text:
        return text.replace('<a ', '<a onclick="window.open(this.href);return false;" ').replace('<A ', '<a onclick="window.open(this.href);return false;" ')
    
    return text
url_open.is_safe = True

@register.filter
def multiply(value, arg):
    return float(value) * float(arg) 
