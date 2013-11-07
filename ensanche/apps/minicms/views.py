# coding=utf-8

from django.utils import translation
from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from models import Page

def page(request,slug=None):
    
    if request.method == "POST":
        if request.POST.get('slug'):
            slug = request.POST.get('slug')
    
    if slug: slug = slug.strip('/')
    
    if not slug or slug == '/':
        page = Page.get_index()
    else:
        page = Page.get_by_slug(slug)
    
    return render_to_response(page.template if page.template else settings.MINICMS_AJAX_BASETEMPLATE, dict(page=page),context_instance=RequestContext(request))

def contact(request):
    
    if request.method <> "POST":
        return HttpResponseBadRequest()
    
    for k in settings.MINICMS_CONTACT_DATA.keys():
        if not request.POST.get(k):
            return HttpResponseBadRequest()
    
    email = ""
    
    for k in settings.MINICMS_CONTACT_DATA.keys():
        email += "%s: %s\n" % (settings.MINICMS_CONTACT_DATA[k],request.POST[k],)
    
    send_mail(settings.MINICMS_CONTACT_SUBJECT, email, settings.MINICMS_CONTACT_FROM, [ settings.MINICMS_CONTACT_TO ], fail_silently=True)
    
    return HttpResponse()


def urllist(request):
    return render_to_response("minicms/urllist.txt",dict(pages=Page.get_all(),site = Site.objects.get_current()),context_instance=RequestContext(request),mimetype="text/plain")
        
