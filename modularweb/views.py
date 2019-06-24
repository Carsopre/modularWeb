from django.http import HttpResponse, Http404
from django.shortcuts import render
from modularweb.models import *

def __colSize(elementList, maxColInRow):
    defaultSize = 12 // maxColInRow
    if elementList is None:
        return defaultSize
    listSize = len(elementList)
    if listSize > 1 and listSize < maxColInRow:
        return 12 // listSize
    return defaultSize

def not_found(request, exception):
    errorMessage = '404. The page you tried to access does not exist.'
    return section(request, 'home', 'index.html', errorMessage)
    
def index(request):
    return section(request, 'home', 'index.html')

def section(request, pageSlug, template='section.html', errorMessage=None):
    variables = []
    sectionPage = MainPage.objects.filter(slug=pageSlug).first()
    if section is None:
        return render(request, template, variables)
    
    socialNetworks = sectionPage.getIconFields()
    if socialNetworks is not None:
        socialNetworks = socialNetworks.filter(isVisible=True)
    snColSize = __colSize(socialNetworks, 12)    
    
    linkedPages = sectionPage.getLinkedPages()
    if linkedPages is not None:
        linkedPages = linkedPages.filter(iconField__isVisible=True)
    lpColSize = __colSize(linkedPages, 4)    
    
    variables = {
        'nbar': 'index',
        'errorMessage': errorMessage,
        'pageName':  BaseField.GetBaseFieldValue('pageName'),
        'mainBg': sectionPage.getBackgroundUrl(),
        'closureBg': sectionPage.getEndBackgroundUrl(),
        'landingMainFields': sectionPage.getLandingFields(LandingPageField.MAINFIELD),
        'landingSubFields': sectionPage.getLandingFields(LandingPageField.SUBFIELD),
        'contentPages': sectionPage.getContentPages(),
        'socialNetworks': socialNetworks, 
        'linkedPages': linkedPages,
        'snColSize': snColSize,
        'lpColSize': lpColSize,
    }
    return render(request, template, variables)

def about(request):
    title = None
    pageName = None
    loadedAbout = Page.GetPage('aboutus')
    if(loadedAbout is not None):
        title = loadedAbout.title
        pageName = loadedAbout.pageName
    variables = {
                    'title': title,
                    'pageName': pageName,
    				'nbar': 'about',
    			}
    return render(request, 'aboutus.html', variables)

def contact(request):
    title = None
    pageName = None
    # We assume we only load one contact (the latest one)
    loadedContact = ContactPage.objects.last()
    if(loadedContact is not None):
        title = loadedContact.title
        pageName = loadedContact.pageName

    variables = {
                    'title': title,
                    'pageName': pageName,
                    'nbar': 'contact',
                    'contact': loadedContact
                }
    return render(request, 'contact.html', variables)

def gallery(request):
    title = None
    pageName = None
    galleryPhotos = None
    # We assume we only load one gallery (the latest one)
    loadedGallery = GalleryPage.objects.last()
    if(loadedGallery is not None):
        galleryPhotos = loadedGallery.getGalleryPhotographies
        title = loadedGallery.title
        pageName = loadedGallery.pageName

    variables = {
                    'title': title,
    				'pageName': pageName,
    				'nbar': 'gallery',
                    'gallery': loadedGallery,
                    'galleryPhotos': galleryPhotos
    			}
    return render(request, 'gallery.html', variables)

def blog(request):
    title = None
    pageName = None
    body = None
    blog = Page.GetPage('blogPage')
    if(blog is not None):
        title = blog.title
        pageName = blog.pageName
    
    variables = {
                    'title': title,
    				'pageName': pageName,
    				'nbar': 'content',
                    'blog': blog
    			}
    return render(request, 'blog.html', variables)
