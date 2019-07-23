from django.test import TestCase
from django.db import models

import pytest
from parameterized import parameterized
from modularweb.models import Photography, BaseField


class Test_BaseField(TestCase):

    __test_base_field = None

    # Django 1.7 requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(Test_BaseField, cls).setUpClass()
        django.setup()

    def setUp(self):
        self.__test_base_field = BaseField.objects.create(
            slug='test_slug',
            name='test_name',
            value='test_value')

    def test_photography_returns_name(self):
        # 1. Verify initial expectations
        self.assertIsNotNone(self.__test_base_field)
        self.assertIsNotNone(self.__test_base_field.name)

        # 2. Verify expectations
        self.assertEqual(
            self.__test_base_field.__str__(),
            self.__test_base_field.name)

    @parameterized.expand([
        ('case_none_value', None),
        ('case_empty_string', ''),
        ('case_wrong_slug', '42')])
    def test_when_get_base_field_value_with_no_arguments_then_does_not_raise(
            self, case_name, search_slug):
        # 1. Set up variables
        found_value = None
        expected_value = ''

        # 2. Run test
        try:
            found_value = BaseField.get_base_field_value(search_slug)
        except Exception as e_error:
            self.fail('Not expected exception, but thrown: {}'.format(
                str(e_error)))

        # 3. Verify expectations
        self.assertEqual(
            found_value,
            expected_value,
            'Expected {} but got {}'.format(
                expected_value, found_value))

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
            self.fail(
                'Not expected exception, but thrown: {}'.format(
                    str(e_error)))

        # 3. Verify expectations
        self.assertEqual(
            found_value, expected_value,
            'Expected {} but got {}'.format(
                expected_value, found_value))
