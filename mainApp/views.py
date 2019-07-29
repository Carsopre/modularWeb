from django.http import HttpResponse, Http404
from django.shortcuts import render
from mainApp.models import *


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
    return render_page(request, 'home', 'index.html', errorMessage)


def index(request):
    return render_page(request, 'scaffold', 'home')


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

    return render(request, template, variables)


def get_content(page_slug):
    base_page = BasePage.get_page(page_slug)
    if(isinstance(base_page, ScaffoldPage)):
        return __get_scaffold(base_page)
    return __get_section(0, base_page)


def __get_scaffold(scaffold_page: ScaffoldPage):
    if scaffold_page is None:
        # To do should be returning 404 not found.
        return None

    content_pages = scaffold_page.get_content_pages()
    section_content_pages = [
        __get_section(contentPage[0], contentPage[1])
        for contentPage in sorted(
            content_pages,
            key=lambda x: x[0])]
    scaffold = {
        'template': 'section_scaffold.html',
        'title': scaffold_page.title,
        'slug': scaffold_page.slug,
        'data': section_content_pages,
    }

    return scaffold


def __get_section(page_order: int, content_page: FlexiblePage):
    if content_page is None:
        return {}

    template = __section_template_map.get(type(content_page))
    variables = content_page.get_property_dict()
    variables['position'] = page_order
    section = {
        'template': template,
        'data': variables,
        'title': content_page.title,
    }

    return section


__section_template_map = {
    IntroPage: 'section_intro.html',
    BlogPage: 'section_blog.html',
    OutroPage: 'section_outro.html',
}
