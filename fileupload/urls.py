from django.conf.urls.defaults import *
from fileupload.views import PdfCreateView, PdfDeleteView

urlpatterns = patterns('',
    (r'^new/$', PdfCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', PdfDeleteView.as_view(), {}, 'upload-delete'),
    url('^pdftohtml/(?P<filename>.*)$', 'fileupload.views.pdftohtml', name="pdftohtml"),
    url('^viewhtml/(?P<fileid>.*)$', 'fileupload.views.viewhtml', name="viewhtml"),
    url('^viewms/(?P<fileid>.*)$', 'fileupload.views.viewmshtml', name="viewmshtml"),
    url('^downloadhtml/$', 'fileupload.views.downloadhtml', name="downloadhtml"),
)

