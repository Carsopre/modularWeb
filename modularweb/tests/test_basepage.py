from django.test import TestCase
from django.db import models
import pytest
from parameterized import parameterized
from modularweb.models import Photography, BasePage


class Test_BasePage(TestCase):
    __test_base_page = None
    __test_base_page_no_bg = None
    __test_fk_bg = None

    def setUp(self):
        self.__test_fk_bg = Photography.objects.create(
            title='test_photography',
            slug='test_slug',
            description='test_description',
            url='test_url')

        self.__test_base_page_no_bg = BasePage.objects.create(
            slug='test_slug_no_bg',
            title='test_title',
            description='test_description',
            url='test_url')

        self.__test_base_page = BasePage.objects.create(
            slug='test_slug',
            title='test_title',
            description='test_description',
            url='test_url',
            background=self.__test_fk_bg)

    def test_basepage_returns_title(self):
        # 1. Verify initial expectations
        self.assertIsNotNone(self.__test_base_page)
        self.assertIsNotNone(self.__test_base_page.title)

        # 2. Verify expectations
        self.assertEqual(
            self.__test_base_page.__str__(),
            self.__test_base_page.title)

    def test_full_url_returns_combination_url_and_slug(self):
        # 1. Set up test model.
        return_value = None
        expected_result = ('test_url\\test_slug')
        # 2. Run test
        try:
            return_value = self.__test_base_page.full_url
        except Exception as e_error:
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify final expectations
        self.assertEqual(return_value, expected_result)

    def test_get_background_url_when_no_background_then_does_not_raise(
            self):
        # 1. Set up initial expectations
        found_result = None
        expected_resut = ''
        nobg_basepage = self.__test_base_page_no_bg
        self.assertIsNotNone(nobg_basepage)

        # 2. Run test
        try:
            found_result = nobg_basepage.get_background_url()
        except Exception as e_error:
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertEqual(
            found_result, expected_resut,
            'Expected {} but got {}'.format(
                found_result, expected_resut))

    def test_get_background_url_when_background_then_returns_expected_string(
            self):
        # 1. Set up initial expectations
        found_result = None
        expected_resut = self.__test_fk_bg.url
        basepage = self.__test_base_page
        self.assertIsNotNone(basepage)

        # 2. Run test
        try:
            found_result = basepage.get_background_url()
        except Exception as e_error:
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertEqual(
            found_result, expected_resut,
            'Expected {} but got {}'.format(
                found_result, expected_resut))

    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42')])
    def test_get_page_when_invalid_slug_then_does_not_raise(
            self, case_name, search_slug):
        # 1. Set up variables
        found_page = None

        # 2. Run test
        try:
            found_page = BasePage.get_page(search_slug)
        except Exception as e_error:
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertIsNone(found_page)

    def test_get_page_when_valid_slug_then_does_not_raise(self):
        # 1. Set up initial expectations
        found_page = None
        expected_page = self.__test_base_page
        self.assertIsNotNone(expected_page)

        # 2. Run test
        try:
            found_page = BasePage.get_page(expected_page.slug)
        except Exception as e_error:
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertEqual(
            found_page,
            expected_page,
            'Expected {} but got {}'.format(found_page, expected_page))
