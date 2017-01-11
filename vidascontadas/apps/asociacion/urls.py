from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from asociacion.views import *
from comercios.views import *

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^propuestas/$', propuestas, name="propuestas"),    
    url(r'^quienes-somos/$', somos, name="quienes-somos"),
    url(r'^contacto/$', contacto, name="contacto"),
    url(r'^buscador/$', buscar_asociados, name="buscador"),
    url(r'^convenios/$', lista_convenios, name="lista-convenios"),
    url(r'^convenios/tipo/(?P<categoria>[\w\-_]+)$', lista_convenios, name="lista-convenios-tipo"),
    url(r'^convenios/(?P<id>[\w\-_]+)/$', detalle_convenio, name="detalle-convenio"),
    url(r'^noticias/$', lista_noticias, name="lista_noticias"),
    url(r'^noticias/(?P<slug>[\w\-_]+)/$', noticia, name="noticia"),
    url(r'^asociate/$', asociate, name="asociate"),
    url(r'^agenda/$', agenda, name="agenda"),
    url(r'^agenda/(?P<slug>[\w\-_]+)/$', evento_fijo, name="evento-fijo"),
    url(r'^agenda/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w\-_]+)/$', evento, name="evento"),
    url(r'^asociados/$', lista_asociados_endless, name="lista-asociados"),   
    url(r'^asociados/(?P<categoria_principal>[\w\-_]+)/$', lista_asociados, name="lista-asociados-by-cat"),  
    url(r'^asociados/(?P<categoria_principal>[\w\-_]+)/(?P<categoria>[\w\-_]+)/$', lista_asociados, name="lista-asociados-by-subcat"), 
  
#    url(r'^eventos/$', "events",name="eventos"),
#    url(r'^comercios/$', "comercios",name="comercios"),
#    url(r'^noticias/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w\-_]+)/$', "news",name="noticia"),
#    url(r'^eventos/(?P<year>\d+)/(?P<slug>[\w\-_]+)/$', "events",name="evento"),
]

urlpatterns += [
    url(r'^mis-comercios/$', cuenta,name="cuenta"),
    url(r'^microsite/$', test, name="test"),
    url(r'^comercios/nuevo/$', NuevaTiendaView, name="nuevo-comercio"),
    url(r'^comercios/modificar/$', NuevaTiendaView, name="modificar-comercio"),
    url(r'^comercios/editar/$', EditarTiendaView, name="editar-comercio"),
    url(r'^comercios/borrar/$', delete_comercio, name="borrar-comercio"),    
    url(r'^comercios/imagen/editar/$', SubirImagenView, name="editar-imagen"),    
    url(r'^comercios/imagen/borrar/$', delete_imagen, name="borrar-imagen"),      
    url(r'^comercios/local/editar/$', ComercioLocalView, name="editar-local"), 
    url(r'^comercios/local/borrar/$', delete_local, name="borrar-local"),     
    url(r'^comercios/pagina/editar/$', ComercioPaginaView, name="editar-pagina"), 
    url(r'^comercios/pagina/borrar/$', delete_pagina, name="borrar-pagina"),     
    url(r'^comercios/propuesta/editar/$', ComercioPropuestaView, name="editar-propuesta"),        
    url(r'^comercios/propuesta/borrar/$', delete_propuesta, name="borrar-propuesta"), 
    url(r'^comercios/(?P<slug>[\w\-_]+)/$', microsite, name="detalle-comercio"),
    url(r'^comercios/(?P<slug>[\w\-_]+)/(?P<id>\d+)/$', propuesta, name="detalle-propuesta"),
    #url(r'^comercios/$', "ListaComerciosView", name="lista-comercio"),
    #url(r'^comercios/(?P<pk>\d+)/edit/$', UpdateOrderView.as_view()),
]