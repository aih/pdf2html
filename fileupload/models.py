from django.db import models

class Pdf(models.Model):

    # This is a small demo using FileField
    file = models.FileField(upload_to="pdf")
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Pdf, self).save(*args, **kwargs)

class Html(models.Model):

    filename = models.SlugField(max_length=50, blank=True)
    fileid = models.CharField(max_length=71, blank=False)
    html = models.TextField()

    def __unicode__(self):
        return self.filename

    @models.permalink
    def get_absolute_url(self):
        return ('viewhtml', [self.fileid] )

    def save(self, *args, **kwargs):
        super(Html, self).save(*args, **kwargs)
