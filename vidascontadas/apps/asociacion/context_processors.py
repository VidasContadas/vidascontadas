from django.conf import settings
from asociacion.models import *

def areacomercial(request):

    try:
        noticias = Noticia.objects.all().order_by('-fecha')[:3]
    except Noticia.DoesNotExist:
        noticias = ''

    try:
        banners = Banner.objects.all()
    except Banner.DoesNotExist:
        banner = ''

    return {
        'ultimas_noticias': noticias,
        'banners': banners,
    }