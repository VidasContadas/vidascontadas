from django import template
from asociacion.models import Evento

register = template.Library()

@register.assignment_tag

def get_banner_url(banners, pagina):
    try:
        banner = banners.get(pagina=pagina)
    except:
        banner = None
        pass
    return banner.imagen.url if banner else '/media/default_banner.png'
