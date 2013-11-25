from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from models import *

def home(request):

	return render_to_response("comercios/home.html",context_instance=RequestContext(request))

def news(request,year=None,month=None,slug=None):

	if not slug:

		noticias = Noticia.get_list()

		return render_to_response("comercios/noticias.html",dict(noticias=noticias),context_instance=RequestContext(request))

	noticia = get_object_or_404(Noticia,fecha__year=year,fecha__month=month,slug=slug)
	otras = Noticia.get_list(exclude=noticia)

	return render_to_response("comercios/noticia.html",dict(noticia=noticia,otras=otras),context_instance=RequestContext(request))

def comercios(request,year=None,month=None,slug=None):

	if not slug:

		comercios = Comercio.get_list()
		categorias = Categoria.get_list()

		return render_to_response("comercios/comercios.html",dict(comercios=comercios,categorias=categorias,),context_instance=RequestContext(request))

	noticia = get_object_or_404(Noticia,fecha__year=year,fecha__month=month,slug=slug)
	otras = Noticia.get_list(exclude=noticia)

	return render_to_response("comercios/noticia.html",dict(noticia=noticia,otras=otras),context_instance=RequestContext(request))