from django.test import TestCase
from django.db import models
from modularweb.models import Photography, BaseField, LandingPageField, BasePage
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

class Test_BasePage(TestCase):
    __test_base_page = None
    __test_base_page_no_bg = None
    __test_fk_bg = None
    def setUp(self):
        self.__test_fk_bg = Photography.objects.create(
            title       =   'test_photography', 
            slug        =   'test_slug',
            description =   'test_description',
            url         =   'test_url')

        self.__test_base_page_no_bg = BasePage.objects.create(
            slug        = 'test_slug_no_bg',
            title       = 'test_title',
            description = 'test_description',
            url         = 'test_url')

        self.__test_base_page = BasePage.objects.create(
            slug        = 'test_slug',
            title       = 'test_title',
            description = 'test_description',
            url         = 'test_url',
            background  = self.__test_fk_bg)
    
    def test_basepage_returns_title(self):      
        # 1. Verify initial expectations
        self.assertIsNotNone(self.__test_base_page)
        self.assertIsNotNone(self.__test_base_page.title)
        
        # 2. Verify expectations
        self.assertEqual(self.__test_base_page.__str__(), self.__test_base_page.title)
    
    def test_full_url_returns_combination_url_and_slug(self):
        # 1. Set up test model.
        return_value = None
        expected_result = ('test_url\\test_slug')
        # 2. Run test
        try:
            return_value = self.__test_base_page.full_url
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify final expectations
        self.assertEqual(return_value, expected_result)
    
    def test_get_background_url_when_no_background_then_does_not_raise_and_returns_empty_string(self):
        # 1. Set up initial expectations
        found_result = None
        expected_resut = ''
        nobg_basepage = self.__test_base_page_no_bg
        self.assertIsNotNone(nobg_basepage)

        # 2. Run test
        try:
            found_result = nobg_basepage.get_background_url()
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_result, expected_resut, 'Expected {} but got {}'.format(found_result, expected_resut))   

    def test_get_background_url_when_background_then_returns_expected_string(self):
        # 1. Set up initial expectations
        found_result = None
        expected_resut = self.__test_fk_bg.url
        basepage = self.__test_base_page
        self.assertIsNotNone(basepage)

        # 2. Run test
        try:
            found_result = basepage.get_background_url()
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_result, expected_resut, 'Expected {} but got {}'.format(found_result, expected_resut))   

    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42')])
    def test_get_page_when_invalid_slug_then_does_not_raise(self, case_name, search_slug):
        # 1. Set up variables
        found_page = None

        # 2. Run test
        try:
            found_page = BasePage.get_page(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
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
            self.fail('Not expected exception, but thrown: {}'.format(str(e_error)))
        
        # 3. Verify expectations
        self.assertEqual(found_page, expected_page, 'Expected {} but got {}'.format(found_page, expected_page))
   