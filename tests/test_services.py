#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_services
----------------------------------

Tests for `teamsupport.services` module.
"""
import unittest

from lxml.builder import E

from teamsupport.services import XMLHTTPServiceClient
from tests import PatchedSessionXmlTests


class TestBaseXMLClient(PatchedSessionXmlTests):

    def setUp(self):
        super(TestBaseXMLClient, self).setUp()
        self.client = XMLHTTPServiceClient(url='https://localhost/')

    def test_parse_xml_response_returns_element(self):
        self.response.content = '<Tickets></Tickets>'
        result = self.client.parse_xml_response(self.response)
        self.assertEqualXml(result, E.Tickets())

    def test_send_as_xml_properly_formats_request(self):
        request_params = {
            'data': {'Field1': 'Test field'},
            'root': 'OuterField',
            'send_as_xml': True
        }
        request_params = self.client._format_xml_request(request_params)

        self.assertEqual(request_params['data'], self.xml_element_string)
        self.assertEqual(
            request_params['headers']['Content-Type'], 'application/xml')

    def test_send_as_xml_properly_formats_xml(self):
        request_element = self.xml_element
        request_params = {
            'data': request_element,
            'send_as_xml': True
        }
        request_params = self.client._format_xml_request(request_params)

        self.assertEqual(request_params['data'], self.xml_element_string)
        self.assertEqual(
            request_params['headers']['Content-Type'], 'application/xml')

    def tearDown(self):
        super(TestBaseXMLClient, self).tearDown()

if __name__ == '__main__':
    unittest.main()
