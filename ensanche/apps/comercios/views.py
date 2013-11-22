from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):

	return render_to_response("comercios/home.html",context_instance=RequestContext(request))

def news(request,slug=None):

	if not slug:
		return render_to_response("comercios/noticias.html",context_instance=RequestContext(request))

	#noticia = get_object_or_404()
	return render_to_response("comercios/noticia.html",context_instance=RequestContext(request))
