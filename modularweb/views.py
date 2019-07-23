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


def section(request, pageSlug, template='section.html', errorMessage=None):
    variables = []
    sectionPage = MainPage.objects.filter(slug=pageSlug).first()
    if sectionPage is None:
        return render(request, template, variables)

    content_pages = sectionPage.get_content_pages()
    section_content_pages = [
        build_sub_section(contentPage[0], contentPage[1])
        for contentPage in sorted(
            content_pages,
            key=lambda x: x[0])]
    # remove top and bottom if existent:
    top_section = get_section_from_list(section_content_pages, 0)
    bottom_section = get_section_from_list(section_content_pages, -1)
    variables = {
        'nbar': 'index',
        'errorMessage': errorMessage,
        'pageName':  BaseField.get_base_field_value('pageName'),
        'top_section': top_section,
        'bottom_section': bottom_section,
        'sub_sections': section_content_pages,
    }
    return render(request, template, variables)


def get_section_from_list(section_list: list, idx: int):
    if not section_list:
        return None
    if len(section_list) > abs(idx):
        return section_list.pop(idx)
    return None


def build_sub_section(pageOrder: int, contentPage: ContentPage):
    """Creates a dictionary of elements necessary to create a html representation
    of a ContentPage

    Arguments:
        pageOrder {int} -- Order in which the page will be shown.
        contentPage {ContentPage} -- Query object representing content page

    Returns:
        Dictionary -- Dictionary to use in the HTML templates
    """
    if contentPage is None:
        return {}

    social_networks = contentPage.get_icon_fields()
    if social_networks is not None:
        social_networks = social_networks.filter(isVisible=True)
    snColSize = __colSize(social_networks, 12)

    linked_pages = contentPage.get_linked_pages()
    if linked_pages is not None:
        linked_pages = linked_pages.filter(iconField__isVisible=True)
    lpColSize = __colSize(linked_pages, 4)

    sub_section = {
        'main_fields': contentPage.get_landing_fields(
            LandingPageField.MAINFIELD),
        'sub_fields': contentPage.get_landing_fields(
            LandingPageField.SUBFIELD),
        'position': pageOrder,
        'background': contentPage.background,
        'body': contentPage.body,
        'linked_pages': contentPage.get_linked_pages(),
        'social_networks': social_networks,
        'linked_pages': linked_pages,
        'snColSize': snColSize,
        'lpColSize': lpColSize,
    }
    return sub_section


def about(request):
    title = None
    pageName = None
    loadedAbout = BasePage.get_page('aboutus')
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
    blog = BasePage.get_page('blogPage')
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
