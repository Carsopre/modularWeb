from django.test import TestCase
from django.db import models
import pytest
from parameterized import parameterized
from modularweb.models import LandingPageField


class Test_LandingPageField(TestCase):
    __test_mf_lp_field = None
    __test_sf_lp_field = None

    def setUp(self):
        self.__test_mf_lp_field = LandingPageField.objects.create(
            slug='test_mf_slug',
            name='test_mf_name',
            value='test_mf_value',
            fieldType=LandingPageField.MAINFIELD)
        self.__test_sf_lp_field = LandingPageField.objects.create(
            slug='test_sf_slug',
            name='test_sf_name',
            value='test_sf_value',
            fieldType=LandingPageField.SUBFIELD)

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
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertIsNotNone(found_value_list)
        self.assertEqual(expected_main_fields, len(found_value_list))
        found_value = found_value_list.first()
        self.assertIsNotNone(found_value)
        self.assertEqual(
            found_value, expected_lp,
            'Expected {} but got {}'.format(
                expected_lp, found_value))

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
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertIsNotNone(found_value_list)
        self.assertEqual(expected_main_fields, len(found_value_list))
        found_value = found_value_list.first()
        self.assertIsNotNone(found_value)
        self.assertEqual(
            found_value, expected_lp,
            'Expected {} but got {}'.format(expected_lp, found_value))
