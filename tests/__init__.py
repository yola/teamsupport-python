# -*- coding: utf-8 -*-

import inspect
import unittest

from lxml import etree
from lxml.builder import E
from mock import Mock, patch
from requests import Response, Session

from teamsupport import init
from teamsupport.services import TeamSupportService


class PatchedSessionTests(unittest.TestCase):
    def setUp(self):
        super(PatchedSessionTests, self).setUp()
        # must patch inspect since it is used on Session.request, and when
        # Session.request is mocked, inspect blows up
        self.request_args = inspect.getargspec(Session.request)
        self.inspect_patcher = patch('demands.inspect.getargspec')
        self.patched_inspect = self.inspect_patcher.start()
        self.patched_inspect.return_value = self.request_args

        self.request_patcher = patch.object(Session, 'request')
        self.request = self.request_patcher.start()
        self.response = Mock(spec=Response(), status_code=200)
        self.request.return_value = self.response

    def tearDown(self):
        self.request_patcher.stop()
        self.inspect_patcher.stop()


class XmlTestCase(unittest.TestCase):
    def setUp(self):
        super(XmlTestCase, self).setUp()
        self.xml_element = E.OuterField(
            E.Field1('Test field')
        )
        self.xml_element_bool_field = E.OuterField(
            E.BoolField('True')
        )
        self.xml_element_empty_field = E.OuterField(
            E.NoneField('')
        )
        self.xml_element_string = etree.tostring(
            self.xml_element, encoding='utf-8', xml_declaration=True,
            pretty_print=True)

    def assertEqualXml(self, first, second, msg=None):
        self.assertEqual(etree.tostring(first), etree.tostring(second), msg)


class PatchedSessionXmlTests(PatchedSessionTests, XmlTestCase):
    pass


class BaseTeamSupportServiceCase(PatchedSessionXmlTests):
    def setUp(self):
        super(BaseTeamSupportServiceCase, self).setUp()
        init('org_id', 'auth_key')
        self.client = TeamSupportService()

    def tearDown(self):
        super(BaseTeamSupportServiceCase, self).tearDown()
