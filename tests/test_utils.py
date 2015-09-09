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
    def setUp(self):
        super(TestToXml, self).setUp()

    def test_to_xml_success_with_data(self):
        params = {
            'data': {'Field1': 'Test field'},
            'root': 'OuterField',
        }
        result = to_xml(**params)

        self.assertEqualXml(result, self.xml_element)

    def tearDown(self):
        super(TestToXml, self).tearDown()


if __name__ == '__main__':
    unittest.main()
