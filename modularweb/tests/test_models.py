from django.test import TestCase
from django.db import models
from modularweb.models import Photography, BaseField, LandingPageField
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
        ('case_wrong_slug', '42')])
    def test_get_photography_without_arguments_does_not_raise_and_returns_none(self, case_name, search_slug):
        # 1. Set up variables
        found_photography = None

        # 2. Run test
        try:
            found_photography = Photography.get_photography(search_slug)
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
            found_photography = Photography.get_photography(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_photography, expected_photography, 'Expected {} but got {}'.format(expected_photography, found_photography))
    
    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42')])
    
    def test_get_photography_url_without_arguments_does_not_raise_and_returns_empty_string(self, case_name, search_slug):
        # 1. Set up variables
        found_url = None
        expected_ulr = ''
        
        # 2. Run test
        try:
            found_url = Photography.get_photography_url(search_slug)
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
            found_url = Photography.get_photography_url(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_url, expected_url, 'Expected {} but got {}'.format(expected_url, found_url))
    
class Test_BaseField(TestCase):

    __test_base_field = None
    def setUp(self):
        self.__test_base_field = BaseField.objects.create(
            slug    =   'test_slug',
            name    =   'test_name',
            value   =   'test_value')

    def test_photography_returns_name(self):      
        # 1. Verify initial expectations
        self.assertIsNotNone(self.__test_base_field)
        self.assertIsNotNone(self.__test_base_field.name)
        
        # 2. Verify expectations
        self.assertEqual(self.__test_base_field.__str__(), self.__test_base_field.name)

    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42')])
    def test_get_base_field_value_without_arguments_does_not_raise_and_returns_empty_string(self, case_name, search_slug):
        # 1. Set up variables
        found_value = None
        expected_value = ''
        
        # 2. Run test
        try:
            found_value = BaseField.get_base_field_value(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_value, expected_value, 'Expected {} but got {}'.format(expected_value, found_value))

    def test_get_base_field_value_with_valid_slug_returns_expected_value(self):
        # 1. Set up initial expectations
        found_value = None
        expected_base_field = self.__test_base_field
        self.assertIsNotNone(self.__test_base_field)
        search_slug = self.__test_base_field.slug
        self.assertIsNotNone(search_slug)
        expected_value = self.__test_base_field.value
        self.assertIsNotNone(expected_value)

        # 2. Run test
        try:
            found_value = BaseField.get_base_field_value(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_value, expected_value, 'Expected {} but got {}'.format(expected_value, found_value))
    
class Test_LandingPageField(TestCase):
    __test_mf_lp_field = None
    __test_sf_lp_field = None
    def setUp(self):
        self.__test_mf_lp_field = LandingPageField.objects.create(
            slug    =   'test_mf_slug',
            name    =   'test_mf_name',
            value   =   'test_mf_value',
            fieldType = LandingPageField.MAINFIELD)
        self.__test_sf_lp_field = LandingPageField.objects.create(
            slug    =   'test_sf_slug',
            name    =   'test_sf_name',
            value   =   'test_sf_value',
            fieldType = LandingPageField.SUBFIELD)
    
    def test_get_main_fields_returns_mainfield_pages(self):
        # 1. Set up initial expectations
        expected_lp = self.__test_mf_lp_field
        expected_main_fields = 1
        self.assertIsNotNone(expected_lp)
        found_value_list = []

        # 2. Run test
        try:
            found_value_list = LandingPageField.get_main_fields()
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertIsNotNone(found_value_list)
        self.assertEqual(expected_main_fields, len(found_value_list))
        found_value = found_value_list.first()
        self.assertIsNotNone(found_value)
        self.assertEqual(found_value, expected_lp, 'Expected {} but got {}'.format(expected_lp, found_value))

    def test_get_sub_fields_returns_subfield_pages(self):
        # 1. Set up initial expectations
        expected_lp = self.__test_sf_lp_field
        expected_main_fields = 1
        self.assertIsNotNone(expected_lp)
        found_value_list = []

        # 2. Run test
        try:
            found_value_list = LandingPageField.get_sub_fields()
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertIsNotNone(found_value_list)
        self.assertEqual(expected_main_fields, len(found_value_list))
        found_value = found_value_list.first()
        self.assertIsNotNone(found_value)
        self.assertEqual(found_value, expected_lp, 'Expected {} but got {}'.format(expected_lp, found_value))