from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})

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

def content_page_01(request):
    variables = {
    				'pageName': 'Content',
    				'nbar': 'content'
    			}
    return render(request, 'content_page_01.html', variables)
