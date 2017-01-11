from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from models import *
from comercios.models import *
import watson
from django.http import Http404

# Create your views here.
def home(request):

    if request.method == 'GET' and 'q' in request.GET:
        raise Http404

    slides = Slides.objects.filter(visible=True).extra(order_by=['order'])
    propuestas = Propuesta.get_last()
    
    return render(request,"home.html",dict(currentpage='home',slides=slides,propuestas=propuestas))

# Create your views here.
def propuestas(request):

    slides = Slides.objects.filter(visible=True).extra(order_by=['order'])
    propuestas = Propuesta.get_list()
    
    return render(request,"propuestas.html",dict(currentpage='home',slides=slides,propuestas=propuestas))


def asociate(request):

    return render(request,"asociate.html",dict(currentpage='asociate'))    

def somos(request):

    return render(request,"quienes_somos.html",dict(currentpage='quienessomos'))  

def contacto(request):

    return render(request,"contacto.html",dict(currentpage='contacto'))       

def lista_convenios(request, categoria = None):
       
    convenios = Convenio.get_list(categoria = categoria)
    categorias = CategoriaConvenio.get_list()

    return render(request,"convenios.html",dict(convenios=convenios, categorias = categorias))

def detalle_convenio(request,id=None):

    convenio = get_object_or_404(Convenio,pk=id)
    categorias = CategoriaConvenio.get_list()
    return render(request,"convenio.html",dict(convenio=convenio, categorias = categorias))    

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
       template = "asociados.html"
    

    return render(request, template,dict(currentpage='asociados', asociados=asociados, categorias=categorias, categoria=categoria))       

#from endless_pagination.decorators import page_template
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

    return render(request, template, context)

#from el_pagination.views import AjaxListView

#class lista_asociados_view(AjaxListView):
#    context_object_name = "asociados"
#    template_name = 'asociados-todos.html'
#    page_template = 'partials/endless_asociados.html'
#
#    def get_queryset(self):
#        return Asociado.objects.all().order_by('nombre')

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
    return render(request, template, context)

def lista_noticias(request):

    noticias = Noticia.get_list()

    return render(request,"noticias.html",dict(currentpage='noticias', noticias=noticias))

def noticia(request, slug):

    noticia = Noticia.objects.get(slug=slug)

    return render(request,"noticia.html",dict(noticia=noticia))

def detalle_noticia(request, year=None, month=None, slug=None):

    if not slug:

        noticias = Noticia.get_list()

        return render(request,"noticias.html",dict(noticias=noticias))

    noticia = get_object_or_404(Noticia,fecha__year=year,fecha__month=month,slug=slug)
    otras = Noticia.get_list(exclude=noticia)

    return render(request,"noticia.html",dict(noticia=noticia, otras=otras))

def agenda(request):

    lista_eventos = Evento.get_list()
    nuestros_eventos = Evento.get_fijos()
    return render(request,"eventos.html",dict(currentpage='agenda', nuestros_eventos=nuestros_eventos, lista_eventos=lista_eventos))

def evento_fijo(request, slug=None):

    evento = get_object_or_404(Evento,fecha_inicio__isnull=True,slug=slug)
    return render(request,"evento.html",dict(evento=evento))

def evento(request, year=None, month=None, slug=None):

    evento = get_object_or_404(Evento,fecha_inicio__year=year,fecha_inicio__month=month,slug=slug)
    return render(request,"evento.html",dict(evento=evento))
