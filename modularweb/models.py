from django.db import models

# Create your models here.
class BasicSettings(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    email = models.CharField(max_length=50)
    def GetAppName(self):
        pass

class Page(models.Model):
    title = models.CharField(max_length=50)
    pageName = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.title

class ContactPage(Page):
    content = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

class Fields(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250)
    contactPage = models.ForeignKey(
                            ContactPage,
                            on_delete=models.CASCADE)

class BlogPage(Page):
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()

class Photography(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=150)
    url = models.URLField(max_length=200)
    def __str__(self):
        return self.title

class GalleryPhotographies(models.Model):
    gallery = models.ForeignKey(
                        Page,
                        on_delete=models.CASCADE)
    photography = models.ForeignKey(
                        Photography,
                        on_delete=models.CASCADE)
    def __str__(self):
        return self.gallery.title + ", " + self.photography.title
    class Meta:
        ordering = ('gallery',)

class GalleryPage(Page):
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()

    def getGalleryPhotographies(self):
        galleryPhotos = GalleryPhotographies.objects.filter( gallery = self )
        photographies = []
        for galleryPhoto in galleryPhotos:
            photographies.append( galleryPhoto.photography )
        return photographies