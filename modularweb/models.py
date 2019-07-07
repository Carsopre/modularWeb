from django.db import models
import os

# Create your models here.
class BasicSettings(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    email = models.CharField(max_length=50)
    def GetAppName(self):
        pass

class Photography(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=150, blank = True)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    def get_photography(slugPhoto):
        return Photography.objects.filter( slug = slugPhoto ).first()
    def get_photography_url(slugPhoto):
        photo = Photography.get_photography(slugPhoto)
        if( photo is None):
            return ""
        return photo.url

class BaseField(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250, null=True, blank=True)
    def get_base_field_value(fieldSlug):
        field = BaseField.objects.filter(slug = fieldSlug).first()
        if field is not None:
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
    def get_main_fields():
        return LandingPageField.objects.filter( fieldType = LandingPageField.MAINFIELD ).all()
    def get_sub_fields():
        return LandingPageField.objects.filter( fieldType = LandingPageField.SUBFIELD ).all()

class IconField(BaseField):
    faIcon = models.CharField(max_length=50)
    faIconType = models.CharField(max_length=50, default="fab")
    isVisible = models.BooleanField(default=True)

class BasePage(models.Model):
    slug = models.SlugField(max_length=25, unique=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null = True, blank=True)
    background = models.ForeignKey(
        Photography,
        null = True,
        blank = True,
        on_delete=models.SET_NULL
    )
    
    @property
    def full_url(self):
        return os.path.join(self.url, self.slug)
    def __str__(self):
        return self.title
    def getBackgroundUrl(self):
        if self.background is None:
            return ''
        return self.background.url
            
    def GetPage(slugPage):
        return Page.objects.filter( slug = slugPage ).first()

class PageLink(models.Model):
    iconField = models.ForeignKey(IconField, on_delete=models.CASCADE)
    basePage = models.ForeignKey(BasePage, on_delete=models.CASCADE)
    def __str__(self):
        return self.basePage.title +" - "+self.iconField.faIcon
    
class ContentPage(BasePage):
    body = models.TextField(blank = True)

class MainPage(BasePage):
    endBackground = models.ForeignKey(
        Photography,
        null = True,
        blank = True,
        on_delete=models.SET_NULL
    )
    fields = models.ManyToManyField(BaseField, blank = True)
    contentPages = models.ManyToManyField(ContentPage, blank = True, related_name='sub_pages')
    linkedPages = models.ManyToManyField(PageLink, blank = True, related_name='linked_pages')

    def getEndBackgroundUrl(self):
        if self.endBackground is None:
            return ''
        return self.endBackground.url
    def getLandingFields(self, ofType):
        return LandingPageField.objects.filter(mainpage=self, fieldType=ofType)
    def getIconFields(self):
        return IconField.objects.filter(mainpage=self)
    def getContentPages(self):
        if self.contentPages.exists():
            return self.contentPages.all()
        return None
    def getLinkedPages(self):
        if self.linkedPages.exists():
            return self.linkedPages.all()
        return None
    
class ContactPage(BasePage):
    content = models.CharField(max_length=50, blank = True)
    email = models.EmailField(blank = True)
    phone = models.CharField(max_length=50, blank = True)
    def GetEmail(slugContact):
        page = ContactPage.objects.filter( slug = slugContact).first()
        if( page is not None):
            return page.email
        return None
    
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

class GalleryPage(BasePage):
    gallery = models.ForeignKey(
                        Gallery,
                        on_delete=models.CASCADE)

    def getGalleryPhotographies(self):
        galleryPhotos = GalleryPhotographies.objects.filter( gallery = self.gallery )
        photographies = []
        for galleryPhoto in galleryPhotos:
            photographies.append( galleryPhoto.photography )
        return photographies