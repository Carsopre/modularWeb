from django.db import models

# Create your models here.
class BasicSettings(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    email = models.CharField(max_length=50)
    def GetAppName(self):
        pass

class PageCategory(models.Model):
    name = models.CharField(max_length=50)
    template = models.CharField(max_length=50)
    def __str__(self):
        return self.name
        
class Page(models.Model):
    name = models.CharField(max_length=50)
    pageCategory = models.ForeignKey(
                        PageCategory, 
                        on_delete=models.CASCADE)
    pageAbsoluteUrl = models.CharField(max_length=50)

class AboutUsPage(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    pageName = models.CharField(max_length=50)

class ContactPage(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    pageName = models.CharField(max_length=50)

class ContentPage(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    def __str__(self):
        return self.title

class Photography(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=150)
    url = models.URLField(max_length=200)
    def __str__(self):
        return self.title

class GalleryPage(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    def __str__(self):
        return self.title
    
    def getGalleryPhotographies(self):
    	galleryPhotos = GalleryPhotographies.objects.filter( gallery = self )
    	photographies = []
    	for galleryPhoto in galleryPhotos:
    		photographies.append( galleryPhoto.photography )
    	return photographies

class GalleryPhotographies(models.Model):
    gallery = models.ForeignKey(
                        GalleryPage,
                        on_delete=models.CASCADE)
    photography = models.ForeignKey(
                        Photography,
                        on_delete=models.CASCADE)
    def __str__(self):
        return self.gallery.title + ", " + self.photography.title
    class Meta:
        ordering = ('gallery',)

class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    pageName = models.CharField(max_length=50)