# coding=utf-8

from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import RequestContext
from models import *

from django.http import  HttpResponseRedirect

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet
from django.forms.models import inlineformset_factory
from forms import *
from cicu.models import UploadedFile
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.contrib.admin.models import ContentType, LogEntry, ADDITION, CHANGE
from django.utils.encoding import force_unicode

#from django.core.exceptions import PermissionDenied

#def edit(request, pk):
#    if not request.user.is_staff:
#        raise PermissionDenied

def test(request):

    return render(request,"microsite.html")    


def microsite(request, slug):

    comercio = get_object_or_404(Comercio,slug=slug)
    propuestas = comercio.propuestas.filter(visible=True)
    return render(request,"comercios/microsite.html",dict(comercio=comercio, propuestas=propuestas))    

def propuesta(request, slug, id):

    comercio = get_object_or_404(Comercio,slug=slug)
    propuestas = comercio.propuestas.filter(visible=True)
    propuesta = get_object_or_404(Propuesta,id=id)
    return render(request,"comercios/propuesta.html",dict(comercio=comercio, propuesta=propuesta, propuestas=propuestas))    


@login_required
def EditarTiendaView(request):
    comercio_id = request.GET.get('id',None)
    comercio = get_object_or_404(Comercio,id=comercio_id)

    if comercio not in request.user.mis_tiendas.all():
        return HttpResponseRedirect(reverse('cuenta'))

    #pagina_form = ComercioPagina()

    return render(request, 'comercios/microsite-editor.html', {
        'comercio': comercio,
        #'nueva_pagina_form': pagina_form,
        })    

@login_required
def NuevaTiendaView(request):

    if request.method == 'POST': # If the form has been submitted...

        if request.GET.get('id',None):
            form = ComercioForm(request.POST, instance=Comercio.objects.get(id=request.GET.get('id')))
            action_flag     = CHANGE
        else:
            form = ComercioForm(request.POST) # A form bound to the POST data
            action_flag     = ADDITION

        if form.is_valid(): # All validation rules pass
            #article = form.save(commit=False)
            #article.user = self.request.user
            #article.save()
            #return HttpResponseRedirect(self.get_success_url())   

            if 'imagen' not in request.POST:
                raise forms.ValidationError('Tienes que subir una imagen.')

            comercio = form.save()
            codigo_imagen = request.POST['imagen']
            if codigo_imagen.isdigit():                
                imagen_url = UploadedFile.objects.get(id=codigo_imagen)
                comercio.imagen = imagen_url.file

            LogEntry.objects.log_action(
                user_id         = request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(comercio).pk,
                object_id       = comercio.pk,
                object_repr     = force_unicode(comercio), 
                action_flag     = action_flag
            )

            #if comercio.imagen == None:
            #    codigo_imagen = request.POST['imagen']
            #    imagen_url = UploadedFile.objects.get(id=codigo_imagen)
            #    comercio.imagen = imagen_url.file

            comercio.administradores.add(request.user)
            comercio.save()
            return HttpResponseRedirect('/comercios/editar/?id='+str(comercio.id))

    else:
        if request.GET.get('id', None):
            form = ComercioForm(instance=Comercio.objects.get(id=request.GET.get('id')))
        else:
            form = ComercioForm()


    return render(request, 'comercios/comercio_form_2.html', {
        'form': form,
        })

@login_required
def SubirImagenView(request):

    if request.method == 'POST': # If the form has been submitted...

        if request.GET.get('id',None):
            form = ImagenCrop(request.POST, instance=Imagen.objects.get(id=request.GET.get('id')))
        else:
            form = ImagenCrop(request.POST) # A form bound to the POST data

        form = ImagenCrop(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            imagen = form.save(commit=False)
            comercio = Comercio.objects.get(id=request.GET.get('comercio'))
            imagen.comercio = comercio

            codigo_imagen = request.POST['imagen']
            if codigo_imagen.isdigit():                
                imagen_url = UploadedFile.objects.get(id=codigo_imagen)
                imagen.imagen = imagen_url.file

            #if imagen.imagen == None:
            #    codigo_imagen = request.POST['imagen']
            #    imagen_url = UploadedFile.objects.get(id=codigo_imagen)                
            #    imagen.imagen = imagen_url.file

            imagen.save()
            return HttpResponseRedirect('/comercios/editar/?id='+str(comercio.id))

    else:
        if request.GET.get('id',None):
            form = ImagenCrop(instance=Imagen.objects.get(id=request.GET.get('id')))
        else:
            form = ImagenCrop()

    return render(request, 'comercios/imagen_form.html', {
        'titulo': u"Subir imágen",
        'form': form,
        })

@login_required
def ComercioLocalView(request):

    if request.method == 'POST': # If the form has been submitted...

        comercio = Comercio.objects.get(id=request.GET.get('comercio'))
        if comercio not in request.user.mis_tiendas.all():
            return HttpResponseRedirect(reverse('cuenta'))

        if request.GET.get('id',None):
            form = ComercioLocal(request.POST, instance=Local.objects.get(id=request.GET.get('id')))
            action_flag     = CHANGE
        else:
            form = ComercioLocal(request.POST) # A form bound to the POST data
            action_flag     = ADDITION

        if form.is_valid(): # All validation rules pass
            local = form.save(commit=False)
            local.comercio = comercio
            local.save()

            LogEntry.objects.log_action(
                user_id         = request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(local).pk,
                object_id       = local.pk,
                object_repr     = force_unicode(local), 
                action_flag     = action_flag
            )
            return HttpResponseRedirect('/comercios/editar/?id='+str(comercio.id))
    else:
        if request.GET.get('id',None):
            form = ComercioLocal(instance=Local.objects.get(id=request.GET.get('id',None)))
        else:
            form = ComercioLocal()

    return render(request, 'comercios/local_form.html', {
        'titulo': u"Añadir local",
        'form': form,
        })

@login_required
def ComercioPaginaView(request):

    if request.method == 'POST': # If the form has been submitted...

        comercio = Comercio.objects.get(id=request.GET.get('comercio'))
        if comercio not in request.user.mis_tiendas.all():
            return HttpResponseRedirect(reverse('cuenta'))

        if request.GET.get('id',None):
            form = ComercioPagina(request.POST, instance=Pagina.objects.get(id=request.GET.get('id')))
        else:
            form = ComercioPagina(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            local = form.save(commit=False)            
            local.comercio = comercio
            local.save()
            return HttpResponseRedirect('/comercios/editar/?id='+str(comercio.id))
    else:
        if request.GET.get('id',None):
            form = ComercioPagina(instance=Pagina.objects.get(id=request.GET.get('id',None)))
        else:
            form = ComercioPagina()

    return render(request, 'comercios/page_form.html', {
        'titulo': u"Añadir página",
        'form': form,
        })

@login_required
def ComercioPropuestaView(request):

    if request.method == 'POST': # If the form has been submitted...

        comercio = Comercio.objects.get(id=request.GET.get('comercio'))
        if comercio not in request.user.mis_tiendas.all():
            return HttpResponseRedirect(reverse('cuenta'))

        if request.GET.get('id',None):
            form = ComercioPropuesta(request.POST, instance=Propuesta.objects.get(id=request.GET.get('id')))
            action_flag     = CHANGE
        else:
            form = ComercioPropuesta(request.POST) # A form bound to the POST data
            action_flag     = ADDITION

        if form.is_valid(): # All validation rules pass
            propuesta = form.save(commit=False)
            propuesta.comercio = comercio
            codigo_imagen = request.POST['imagen']
            if codigo_imagen.isdigit():                
                imagen_url = UploadedFile.objects.get(id=codigo_imagen)
                propuesta.imagen = imagen_url.file
            propuesta.save()


            LogEntry.objects.log_action(
                user_id         = request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(propuesta).pk,
                object_id       = propuesta.pk,
                object_repr     = force_unicode(propuesta), 
                action_flag     = action_flag
            )

            return HttpResponseRedirect('/comercios/editar/?id='+str(comercio.id))

    else:
        if request.GET.get('id',None):
            form = ComercioPropuesta(instance=Propuesta.objects.get(id=request.GET.get('id')))
        else:
            form = ComercioPropuesta()

    return render(request, 'comercios/propuesta_form.html', {
        'titulo': u"Nueva propuesta",
        'form': form,
        })
    
@login_required
def cuenta(request):

    tiendas = request.user.mis_tiendas.all()
    return render(request,"mis-tiendas.html",dict(tiendas=tiendas))  

@login_required
def delete_comercio(request):

    comercio = Comercio.objects.get(id=request.GET.get('id'))
    if comercio not in request.user.mis_tiendas.all():
            return HttpResponseRedirect(reverse('cuenta'))

    comercio.delete()
    return HttpResponseRedirect('/mis-comercios/')

@login_required
def delete_propuesta(request):

    obj = Propuesta.objects.get(id=request.GET.get('id'))
    if obj.comercio not in request.user.mis_tiendas.all():
        return HttpResponseRedirect(reverse('cuenta'))

    obj.delete()
    return HttpResponseRedirect('/comercios/editar/?id='+str(obj.comercio.id))


@login_required
def delete_imagen(request):

    obj = Imagen.objects.get(id=request.GET.get('id'))
    if obj.comercio not in request.user.mis_tiendas.all():
        return HttpResponseRedirect(reverse('cuenta'))
    obj.delete()
    return HttpResponseRedirect('/comercios/editar/?id='+str(obj.comercio.id))

@login_required
def delete_local(request):

    obj = Local.objects.get(id=request.GET.get('id'))
    if obj.comercio not in request.user.mis_tiendas.all():
        return HttpResponseRedirect(reverse('cuenta'))
    obj.delete()
    return HttpResponseRedirect('/comercios/editar/?id='+str(obj.comercio.id))

@login_required
def delete_pagina(request):

    obj = Pagina.objects.get(id=request.GET.get('id'))
    if obj.comercio not in request.user.mis_tiendas.all():
        return HttpResponseRedirect(reverse('cuenta'))
    obj.delete()
    return HttpResponseRedirect('/comercios/editar/?id='+str(obj.comercio.id))

def events(request, year=None, month=None, slug=None):

	if not slug:

		eventos = Evento.get_list()

		return render(request,"comercios/eventos.html",dict(eventos=eventos))

	evento = get_object_or_404(Evento,fecha_inicio__year=year,slug=slug)
	otras = Evento.get_list(exclude=evento)

	return render(request,"comercios/evento.html",dict(evento=evento,otras=otras))


def comercios(request,year=None,month=None,slug=None):

	if not slug:

		comercios = Comercio.get_list()
		categorias = CategoriaComercio.get_list()

		return render(request,"comercios/comercios.html",dict(comercios=comercios,categorias=categorias,))

	noticia = get_object_or_404(Noticia,fecha__year=year,fecha__month=month,slug=slug)
	otras = Noticia.get_list(exclude=noticia)

	return render(request,"comercios/noticia.html",dict(noticia=noticia,otras=otras))