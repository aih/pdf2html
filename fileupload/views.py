from fileupload.models import Pdf, Html
from fileupload.utils.fileconvert import convertpdf2html 
from django.views.generic import CreateView, DeleteView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from lxml import etree

from django.conf import settings
import uuid, os


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

def pdftohtml(request, filename): 
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        fname =  GET['filename']
        if fname[-4:] == '.pdf': #change this to validate actual pdf file format
            ispdf = True
            pdfpath =  os.path.join(settings.MEDIA_ROOT, 'pdf', fname)
            print pdfpath
            htmltxt = convertpdf2html(pdfpath)
            fname = fname[:-4]
            fileid = uuid.uuid4().urn.split(':')[2].replace('-','')[:16]+'.html'
            #htmlurl = fname + fileid +'.html'
            htmlobj = Html(filename = fname, fileid = fileid, html = htmltxt)
            htmlobj.save()
            htmlurl = htmlobj.get_absolute_url()
            print 'htmlurl: ' + htmlurl
            results = {'success': True, 'ispdf' : True, 'hash': htmlurl}
        else:
            ispdf = False
            results = {'success': False, 'ispdf' : ispdf, 'hash': 'Not PDF'}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')

def viewhtml(request, fileid):
    htmlobj = Html.objects.get(fileid = fileid)
    return render_to_response('viewhtml/converted.html', {'htmltxt': htmlobj.html}, mimetype="application/xhtml+xml")

def viewmshtml(request, fileid):
    htmlobj = Html.objects.get(fileid = fileid)
    root = etree.XML(htmlobj.html)
    body = etree.tostring(root, pretty_print = True)
    return render_to_response('viewhtml/msconverted.html', {'htmltxt': body, 'filename' : htmlobj.filename}, mimetype="application/xhtml+xml")

def downloadhtml(request):
    return HttpResponse(json, mimetype='application/json') 
