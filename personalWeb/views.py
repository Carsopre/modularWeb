from django.http import HttpResponse, Http404
from django.shortcuts import render
from personalWeb.models import *


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
    return render_scaffold(request, 'home', 'index.html', errorMessage)


def index(request):
    return render_scaffold(request, 'home')


def render_scaffold(
        request, pageSlug, template='scaffold.html', errorMessage=None):
    variables = {}
    scaffold_page = ScaffoldPage.get_page(slug_page=pageSlug)
    if scaffold_page is None:
        # To do should be returning 404 not found.
        return render(request, template, variables)

    content_pages = scaffold_page.get_content_pages()
    section_content_pages = [
        get_section(contentPage[0], contentPage[1])
        for contentPage in sorted(
            content_pages,
            key=lambda x: x[0])]
    variables = {
        'nbar': 'index',
        'errorMessage': errorMessage,
        'page_name':  scaffold_page.title,
        'scaffold_sections': section_content_pages,
    }
    return render(request, template, variables)


def render_section(
        request, pageSlug, template='section.html', errorMessage=None):
    pass


def get_section(page_order: int, content_page: ContentPage):
    """Creates a dictionary of elements necessary to create a html representation
    of a ContentPage

    Arguments:
        page_order {int} -- Order in which the page will be shown.
        content_page {ContentPage} -- Query object representing content page

    Returns:
        Dictionary -- Dictionary to use in the HTML templates
    """
    if content_page is None:
        return {}

    template = __section_template_map.get(content_page.page_type)
    variables = {
        'position': page_order,
        'title': content_page.title,
        'slug': content_page.slug,
        'body': content_page.body,
        'background': content_page.background_url,
    }

    section = {
        'template': template,
        'data': variables,
    }

    return section

__section_template_map = {
    ContentPageType.INTRO_PAGE: 'section_intro.html',
    ContentPageType.BLOG_PAGE: 'section_blog.html',
    ContentPageType.OUTRO_PAGE: 'section_outro.html',
}
