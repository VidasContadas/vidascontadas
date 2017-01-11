from django.shortcuts import render, render_to_response,get_object_or_404
from django.template import RequestContext
from models import *
from comercios.models import *
import watson

# Create your views here.
def home(request):

    slides = Slides.objects.filter(visible=True).extra(order_by=['order'])
    propuestas = Propuesta.get_last()
    
    return render_to_response("home.html",dict(currentpage='home',slides=slides,propuestas=propuestas),context_instance=RequestContext(request))

# Create your views here.
def propuestas(request):

    slides = Slides.objects.filter(visible=True).extra(order_by=['order'])
    propuestas = Propuesta.get_list()
    
    return render_to_response("propuestas.html",dict(currentpage='home',slides=slides,propuestas=propuestas),context_instance=RequestContext(request))


def asociate(request):

    return render_to_response("asociate.html",dict(currentpage='asociate'),context_instance=RequestContext(request))    

def somos(request):

    return render_to_response("quienes_somos.html",dict(currentpage='quienessomos'),context_instance=RequestContext(request))  

def contacto(request):

    return render_to_response("contacto.html",dict(currentpage='contacto'),context_instance=RequestContext(request))       

def lista_convenios(request, categoria = None):
       
    convenios = Convenio.get_list(categoria = categoria)
    categorias = CategoriaConvenio.get_list()

    return render_to_response("convenios.html",dict(convenios=convenios, categorias = categorias),context_instance=RequestContext(request))

def detalle_convenio(request,id=None):

    convenio = get_object_or_404(Convenio,pk=id)
    categorias = CategoriaConvenio.get_list()
    return render_to_response("convenio.html",dict(convenio=convenio, categorias = categorias),context_instance=RequestContext(request))    

def lista_asociados(request, categoria_principal = None, categoria = None):

    categorias = CategoriaAsociado.get_list()

    if categoria_principal and not categoria:        
        categoria = CategoriaAsociado.objects.get(slug=categoria_principal)
        asociados = categoria.asociados.all().order_by('nombre')
        for c in categoria.children.all():
            asociados = asociados | c.asociados.all().order_by('nombre')
        template = "asociados.html"

    elif categoria:        
        categoria = CategoriaAsociado.objects.get(slug=categoria)
        asociados = categoria.asociados.all().order_by('nombre')
        template = "asociados.html"

    else:
       asociados = Asociado.get_list()
       template = "asociados-todos.html"
    

    return render_to_response(template,dict(currentpage='asociados', asociados=asociados, categorias=categorias, categoria=categoria),context_instance=RequestContext(request))       

from endless_pagination.decorators import page_template

#@page_template('partials/endless_asociados.html') 
def lista_asociados_endless(
        request, template='asociados-todos.html', page_template='partials/endless_asociados.html',extra_context=None):
    context = {
        'asociados': Asociado.objects.all().order_by('nombre'),
        'categorias': CategoriaAsociado.get_list(),
        'page_template': page_template,
        'currentpage':'asociados'
    }
    if request.is_ajax():
        template = page_template
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))

#@page_template('partials/endless_asociados.html') 
def buscar_asociados(
        request, template='buscador.html', page_template='partials/endless_asociados.html',extra_context=None):
    
    request.encoding = 'utf-8'
    if request.method == 'POST': # If the form has been submitted...
        query = request.POST['query']
        asociados = watson.filter(Asociado,query)
    else:
        asociados =  Asociado.objects.all().order_by('nombre')
        query = None

    context = {
        'asociados': asociados,   
        'query': query,     
        'categorias': CategoriaAsociado.get_list(),
        'page_template': page_template
    }
    if request.is_ajax():
        template = page_template
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))

def lista_noticias(request):

    noticias = Noticia.get_list()

    return render_to_response("noticias.html",dict(currentpage='noticias', noticias=noticias),context_instance=RequestContext(request))

def noticia(request, slug):

    noticia = Noticia.objects.get(slug=slug)

    return render_to_response("noticia.html",dict(noticia=noticia),context_instance=RequestContext(request))

def detalle_noticia(request, year=None, month=None, slug=None):

    if not slug:

        noticias = Noticia.get_list()

        return render_to_response("noticias.html",dict(noticias=noticias),context_instance=RequestContext(request))

    noticia = get_object_or_404(Noticia,fecha__year=year,fecha__month=month,slug=slug)
    otras = Noticia.get_list(exclude=noticia)

    return render_to_response("noticia.html",dict(noticia=noticia, otras=otras),context_instance=RequestContext(request))

def agenda(request):

    lista_eventos = Evento.get_list()
    nuestros_eventos = Evento.get_fijos()
    return render_to_response("eventos.html",dict(currentpage='agenda', nuestros_eventos=nuestros_eventos, lista_eventos=lista_eventos),context_instance=RequestContext(request))

def evento_fijo(request, slug=None):

    evento = get_object_or_404(Evento,fecha_inicio__isnull=True,slug=slug)
    return render_to_response("evento.html",dict(evento=evento),context_instance=RequestContext(request))

def evento(request, year=None, month=None, slug=None):

    evento = get_object_or_404(Evento,fecha_inicio__year=year,fecha_inicio__month=month,slug=slug)
    return render_to_response("evento.html",dict(evento=evento),context_instance=RequestContext(request))
