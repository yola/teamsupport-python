#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `teamsupport.utils` module.
"""
import unittest

from lxml import etree

from teamsupport.utils import to_xml
from tests import XmlTestCase


class TestToXml(XmlTestCase):
    def setUp(self):
        super(TestToXml, self).setUp()

    def test_to_xml_success_with_data(self):
        params = {
            'data': {'Field1': 'Test field'},
            'root': 'OuterField',
        }
        result = to_xml(**params)

        root_element = etree.Element('OuterField')
        sub_element = etree.SubElement(root_element, 'Field1')
        sub_element.text = 'Test field'

        self.assertEqualXml(result, root_element)

    def test_to_xml_success_with_cdata(self):
        params = {
            'cdata': {'Field2URL': "<a href='https://localhost/test'>test<a>"},
            'root': 'OuterField',
        }
        result = to_xml(**params)

        root_element = etree.Element('OuterField')
        sub_element = etree.SubElement(root_element, 'Field2URL')
        sub_element.text = etree.CDATA(
            "<a href='https://localhost/test'>test<a>")

        self.assertEqualXml(result, root_element)

    def test_to_xml_raises_exception_without_data_or_cdata(self):
        self.assertRaises(TypeError, to_xml, 'OuterField')

    def tearDown(self):
        super(TestToXml, self).tearDown()


if __name__ == '__main__':
    unittest.main()
