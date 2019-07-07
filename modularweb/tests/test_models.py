from django.test import TestCase
import unittest
from django.db import models
from modularweb.models import Photography
from parameterized import parameterized

class Test_Photography(TestCase):
    __test_photography = None
    def setUp(self):
        self.__test_photography = Photography.objects.create(
            title       =   'test_photography', 
            slug        =   'test_slug',
            description =   'test_description',
            url         =   'test_url')

    def test_photography_returns_title(self):      
        # 1. Verify initial expectations
        self.assertIsNotNone(self.__test_photography)
        self.assertIsNotNone(self.__test_photography.title)
        
        # 2. Verify expectations
        self.assertEqual(self.__test_photography.__str__(), self.__test_photography.title)
    
    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42'),
    ])
    def test_get_photography_without_arguments_does_not_raise_and_returns_none(self, case_name, search_slug):
        # 1. Set up variables
        found_photography = None

        # 2. Run test
        try:
            found_photography = Photography.GetPhotography(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertIsNone(found_photography)

    def test_get_photography_with_valid_slug_returns_expected_photography(self):
        # 1. Set up initial expectations
        found_photography = None
        expected_photography = self.__test_photography
        self.assertIsNotNone(self.__test_photography)
        search_slug = self.__test_photography.slug
        self.assertIsNotNone(search_slug)

        # 2. Run test
        try:
            found_photography = Photography.GetPhotography(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_photography, expected_photography, 'Expected {} but got {}'.format(expected_photography, found_photography))
    
    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42'),
    ])
    def test_get_photography_url_without_arguments_does_not_raise_and_returns_empty_string(self, case_name, search_slug):
        # 1. Set up variables
        found_url = None
        expected_ulr = ''
        
        # 2. Run test
        try:
            found_url = Photography.GetPhotographyUrl(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_url, expected_ulr, 'Expected {} but got {}'.format(expected_ulr, found_url))

    def test_get_photography_url_with_valid_slug_returns_expected_url(self):
        # 1. Set up initial expectations
        found_url = None
        expected_photography = self.__test_photography
        self.assertIsNotNone(self.__test_photography)
        search_slug = self.__test_photography.slug
        self.assertIsNotNone(search_slug)
        expected_url = self.__test_photography.url
        self.assertIsNotNone(expected_url)

        # 2. Run test
        try:
            found_url = Photography.GetPhotographyUrl(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_url, expected_url, 'Expected {} but got {}'.format(expected_photography, found_photography))
    


