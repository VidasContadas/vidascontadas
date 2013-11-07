from django.http import HttpResponseRedirect
from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    """
    A base model admin to use in providing access to to logically deleted
    objects.
    """
    
    list_display = ("__unicode__", "deleted")
    list_display_filter = ("deleted",)
    exclude = ('date_created','date_modified','date_removed','deleted')
    
    def queryset(self, request):
        qs = self.model._default_manager.all_with_deleted()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def changelist_view(self, request, extra_context=None):
        if not request.GET.has_key('deleted__exact'):

            q = request.GET.copy()
            q['deleted__exact'] = 0
            request.GET = q

            return HttpResponseRedirect(request.path+"?"+request.GET.urlencode())
        
        return super(ModelAdmin,self).changelist_view(request, extra_context=extra_context)
