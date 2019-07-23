from django.test import TestCase
from django.db import models
import pytest
from parameterized import parameterized
from modularweb.models import ContentPage
from modularweb.models import LibraryPage, PageLink, IconField


class Test_ContentPage(TestCase):
    __test_content_page = None
    __test_linked_page = None
    __test_linked_pages = []

    def setUp(self):
        self.__test_linked_page = LibraryPage.objects.create(
            slug='test_slug_linked_page',
            title='test_title',
            description='test_description',
            url='test_url',
            category='new_category'
        )
        self.__test_linked_pages.append(self.__test_linked_page)
        self.__test_content_page = ContentPage.objects.create(
            slug='test_slug_content_page',
            title='test_title',
            description='test_description',
            url='test_url')
        icon_field = IconField.objects.create(
            faIcon='fa-dummy'
        )
        page_link = PageLink.objects.create(
            basePage=self.__test_linked_page,
            iconField=icon_field
        )
        self.__test_content_page.linkedPages.add(page_link)

    def test_get_library_list_returns_libaries(self):
        # 1. Verify initial expectations
        self.assertIsNotNone(self.__test_linked_page)
        self.assertIsNotNone(self.__test_linked_pages)
        self.assertIsNotNone(self.__test_content_page)

        # 2. Verify expectations
        library_list = self.__test_content_page.get_library_list()

        # 3. Verify expectations
        self.assertIsNotNone(library_list)
        library_page = library_list[0]
        self.assertIsNotNone(library_page)
        self.assertEqual(
            library_page.basePage,
            self.__test_linked_page
        )
