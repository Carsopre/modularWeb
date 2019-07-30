from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render
from portFolioApp.models import *

from mainApp.views import render_page as rp


# Create your views here.
def render_page(
        request, page_type, page_slug, template='index.html', errorMessage=None):
    breadcrumbs = None
    title = None

    section = get_content(page_slug)
    if section:
        title = section.get('title')

    variables = {
        'nbar': 'index',
        'errorMessage': errorMessage,
        'page_name':  title,
        'breadcrumbs': breadcrumbs,
        'section': section,
    }

    return rp(request, template, variables)
