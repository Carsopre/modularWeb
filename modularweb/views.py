from django.http import HttpResponse
from django.shortcuts import render
from modularweb.models import ContentPage

def index(request):
    variables = {
    				'nbar': 'index'
    			}
    return render(request, 'index.html', variables)

def contact(request):
    variables = {
    				'pageName': 'Contact',
    				'nbar': 'contact'
    			}
    return render(request, 'contact.html', variables)

def about(request):
    variables = {
    				'pageName': 'About us',
    				'nbar': 'about'
    			}
    return render(request, 'aboutus.html', variables)

def gallery(request):
    variables = {
    				'pageName': 'Gallery',
    				'nbar': 'gallery'
    			}
    return render(request, 'gallery.html', variables)

def content_page(request):
    try:
        content = ContentPage.objects.first()
        pass
    except Exception as e:
        raise Http404("Content not found")
    
    variables = {
    				'pageName': 'Content',
    				'nbar': 'content',
                    'title': content.title,
                    'body': content.body
    			}
    return render(request, 'content_page.html', variables)
