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
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField(blank = True)
    def __str__(self):
        return self.title
    def GetPage(slugPage):
        return Page.objects.filter( slug = slugPage ).first()

class ContactPage(Page):
    content = models.CharField(max_length=50, blank = True)
    email = models.EmailField(blank = True)
    phone = models.CharField(max_length=50, blank = True)
    def GetEmail(slugContact):
        page = ContactPage.objects.filter( slug = slugContact).first()
        if( page is not None):
            return page.email
        return None

    

class BaseField(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250)

    def GetContactFieldValue(fieldSlug):
        field = BaseField.objects.filter(slug = fieldSlug).first()
        if(field is not None):
            return field.value
        return ""
    def __str__(self):
        return self.name
    
class LandingPageField(BaseField):
    MAINFIELD = 'MF'
    SUBFIELD = 'SF'
    FIELD_TYPES = [
        (MAINFIELD, 'Main field (h2)'),
        (SUBFIELD, 'Sub field (h3)')
    ]
    fieldType = models.CharField(
        max_length=2,
        choices=FIELD_TYPES,
        default=MAINFIELD,
    )
    def getMainFields():
        return LandingPageField.objects.filter( fieldType = LandingPageField.MAINFIELD ).all()
    def getSubFields():
        return LandingPageField.objects.filter( fieldType = LandingPageField.SUBFIELD ).all()

class ContactField(BaseField):
    faIcon = models.CharField(max_length=50)
    faIconType = models.CharField(max_length=50, default="fab")
    isVisible = models.BooleanField(default=True)
    
class Photography(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=150, blank = True)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    def GetPhotography(slugPhoto):
        return Photography.objects.filter( slug = slugPhoto ).first()
    def GetPhotographyUrl(slugPhoto):
        photo = Photography.GetPhotography(slugPhoto)
        if( photo is not None):
            return photo.url
        ""

class Gallery(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self):
        return self.slug
    def GetGalleryPhotographies(self):
        galleryPhotos = GalleryPhotographies.objects.filter( gallery = self )
        photographies = []
        for galleryPhoto in galleryPhotos:
            photographies.append( galleryPhoto.photography )
        return photographies
    def GetGalleryPhoto(self, photoSlug):
        photoGallery = GalleryPhotographies.objects.filter(gallery = self, photography__slug = photoSlug).first()
        if(photoGallery is not None):
            return photoGallery.photography
        return None
    
class GalleryPhotographies(models.Model):
    gallery = models.ForeignKey(
                        Gallery,
                        on_delete=models.CASCADE)
    photography = models.ForeignKey(
                        Photography,
                        on_delete=models.CASCADE)
    def __str__(self):
        return self.gallery.slug + ", " + self.photography.title
    class Meta:
        ordering = ('gallery',)

class GalleryPage(Page):
    gallery = models.ForeignKey(
                        Gallery,
                        on_delete=models.CASCADE)

    def getGalleryPhotographies(self):
        galleryPhotos = GalleryPhotographies.objects.filter( gallery = self.gallery )
        photographies = []
        for galleryPhoto in galleryPhotos:
            photographies.append( galleryPhoto.photography )
        return photographies