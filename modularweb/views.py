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
    return section(request, 'home')


def main_view(request, pageSlug, template='section.html', errorMessage=None):
    variables = []
    scaffold_page = ScaffoldPage.objects.filter(
        slug=pageSlug
    ).first()
    if scaffold_page is None:
        # to-do should be returning error message not found
        return not_found(request, None)


def section(request, pageSlug, template='section.html', errorMessage=None):
    variables = []
    # Assume scaffold page for now
    section_page = ScaffoldPage.objects.filter(
        slug=pageSlug
    ).first()

    if section_page is None:
        # to-do should be returning error message not found
        return not_found(request, None)

    content_pages = section_page.get_content_pages()
    section_list = [
        get_section(contentPage[0], contentPage[1])
        for contentPage in sorted(
            content_pages,
            key=lambda x: x[0])]

    variables = {
        'nbar': 'index',
        'errorMessage': errorMessage,
        'pageName':  section_page.title,
        'section_list': section_list,
    }

    return render(request, 'main_page.html', variables)


def get_section(pageOrder: int, sectionPage: BasePage):
    """Creates a dictionary of elements necessary to create a html representation
    of a BasePage

    Arguments:
        pageOrder {int} -- Order in which the page will be shown.
        basePage {BasePage} -- Query object representing content page

    Returns:
        Dictionary -- Dictionary to use in the HTML templates
    """
    if sectionPage is None:
        return {}

    section_data = {
        'position': pageOrder,
        'slug': sectionPage.slug,
        'title': sectionPage.title,
        'url': sectionPage.url,
        'background': sectionPage.background,
    }
    section_template = 'section_basic.html'

    return {
        'template': section_template,
        'data': section_data
    }
