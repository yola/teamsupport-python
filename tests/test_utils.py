#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `teamsupport.utils` module.
"""
import unittest

from teamsupport.utils import to_xml
from tests import XmlTestCase


class TestToXml(XmlTestCase):
    def test_to_xml_succeeds_with_text_data(self):
        params = {
            'data': {'Field1': 'Test field'},
            'root': 'OuterField',
        }
        result = to_xml(**params)
        self.assertEqualXml(result, self.xml_element)

    def test_to_xml_succeeds_with_non_text_data(self):
        params = {
            'data': {'BoolField': True},
            'root': 'OuterField',
        }
        result = to_xml(**params)
        self.assertEqualXml(result, self.xml_element_bool_field)

    def test_to_xml_succeeds_with_none_value(self):
        params = {
            'data': {'NoneField': None},
            'root': 'OuterField',
        }
        result = to_xml(**params)
        self.assertEqualXml(result, self.xml_element_empty_field)


if __name__ == '__main__':
    unittest.main()
