from django.http import HttpResponse, Http404
from django.shortcuts import render
from modularweb.models import Gallery, ContactPage, Page, GalleryPage, Photography, Fields

def index(request):
    gallery = Gallery.objects.filter(slug='indexBgs').first()
    variables = {
                'nbar': 'index',
                'pageName':  ContactPage.GetContactFieldValue('pageName'),
                'about': Page.objects.filter(slug='indexAbout').first(),
                'mainBg': Photography.GetPhotographyUrl('mainBg'),
                'middleBg': Photography.GetPhotographyUrl('middleBg'),
                'closureBg': Photography.GetPhotographyUrl('closureBg'),
                'indexText1': ContactPage.GetContactFieldValue('indexText1'),
                'indexText2': ContactPage.GetContactFieldValue('indexText2'),
                'indexText3': ContactPage.GetContactFieldValue('indexText3'),
                'indexText4': ContactPage.GetContactFieldValue('indexText4'),
                'indexTextWork': ContactPage.GetContactFieldValue('indexTextWork'),
                'linkedin': ContactPage.GetContactFieldValue('linkedin'),
                'github': ContactPage.GetContactFieldValue( 'github'),
                'email': ContactPage.GetEmail('indexContact'),
                'facebook': ContactPage.GetContactFieldValue('facebook'),
                'flickr': ContactPage.GetContactFieldValue( 'flickr'),
                'instagram': ContactPage.GetContactFieldValue( 'instagram')        
            }
    return render(request, 'index.html', variables)

def about(request):
    title = None
    pageName = None
    # We assume we only load one contact (the latest one)
    loadedContact = BlogPage.objects.filter(pageName='aboutus').last()
    if(loadedContact is not None):
        title = loadedContact.title
        pageName = loadedContact.pageName
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
    blog = BlogPage.objects.filter(pageName='blogPage').last()
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
