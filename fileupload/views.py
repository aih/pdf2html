from fileupload.models import Pdf
from django.views.generic import CreateView, DeleteView

from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class PdfCreateView(CreateView):
    model = Pdf

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "pdf/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + "pdf/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PdfDeleteView(DeleteView):
    model = Pdf
    
    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

def pdftohtml(request): 
    results = {'success':False}

    if request.method == u'GET':
        GET = request.GET
        # Convert to html and get result
        # if successful:
        #     converted = 'True'
        #     create hash for url
        test = 1 + 1
        if test == 2:
            htmlurl = str(test)+'.html'
            results = {'success': True, 'hash': htmlurl}
        else:
            results = {'success': False, 'hash': ''}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')
