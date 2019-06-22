from django.http import HttpResponse, Http404
from django.shortcuts import render
from modularweb.models import Gallery, ContactPage, Page, GalleryPage, Photography, BaseField, ContactField

def index(request):
    gallery = Gallery.objects.filter(slug='indexBgs').first()
    variables = {
                'nbar': 'index',
                'about': Page.objects.filter(slug='indexAbout').first(),
                'email': ContactPage.GetEmail('indexContact'),
                'mainBg': Photography.GetPhotographyUrl('mainBg'),
                'middleBg': Photography.GetPhotographyUrl('middleBg'),
                'closureBg': Photography.GetPhotographyUrl('closureBg'),
                'pageName':  BaseField.GetContactFieldValue('pageName'),
                'indexText1': BaseField.GetContactFieldValue('indexText1'),
                'indexText2': BaseField.GetContactFieldValue('indexText2'),
                'indexText3': BaseField.GetContactFieldValue('indexText3'),
                'indexText4': BaseField.GetContactFieldValue('indexText4'),
                'indexTextWork': BaseField.GetContactFieldValue('indexTextWork'),
                'socialNetworks':ContactField.objects.filter(isVisible=True).all(),
#                'linkedin': Fields.GetContactFieldValue('linkedin'),
#                'github': Fields.GetContactFieldValue( 'github'),
#                'facebook': Fields.GetContactFieldValue('facebook'),
#                'flickr': Fields.GetContactFieldValue( 'flickr'),
#                'instagram': Fields.GetContactFieldValue( 'instagram')        
            }
    return render(request, 'index.html', variables)

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
