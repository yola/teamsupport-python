#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_models
----------------------------------

Tests for `teamsupport.models` module.
"""
import unittest

from lxml import etree

from teamsupport.models import Action, Ticket
from tests import BaseTeamSupportServiceCase


class TestTicket(BaseTeamSupportServiceCase):
    def test_initialisation_with_id(self):
        self.response.content = """<Ticket><TicketID>ID</TicketID></Ticket>"""

        ticket = Ticket(self.client, ticket_id='ID')
        self.assertEqual(ticket.id, 'ID')

    def test_initialisation_with_data(self):
        ticket_element = etree.fromstring(
            """<Ticket><TicketID>ID</TicketID></Ticket>""")
        ticket = Ticket(self.client, data=ticket_element)
        self.assertEqual(ticket.id, 'ID')

    def test_initialisation_fails_when_missing_args(self):
        self.assertRaises(TypeError, Ticket, self.client)

    def test_getattr(self):
        ticket_element = etree.fromstring("""<Ticket>
                <TicketID>ID</TicketID><Field2>Test</Field2>
            </Ticket>""")
        ticket = Ticket(self.client, data=ticket_element)
        self.assertEqual(ticket.Field2, 'Test')

    def test_actions_property(self):
        self.response.content = """<Actions>
            <Action>
                <ID>ActionID</ID>
                <TicketID>ID</TicketID>
                <Name>Description</Name>
            </Action>
        </Actions>"""

        ticket_element = etree.fromstring(
            """<Ticket><TicketID>ID</TicketID></Ticket>""")
        ticket = Ticket(self.client, data=ticket_element)

        actions = ticket.actions
        self.assertEqual(len(actions), 1)
        self.assertIsInstance(actions[0], Action)
        self.assertEqual(actions[0].id, 'ActionID')
        self.assertEqual(actions[0].ticket_id, 'ID')
        self.assertEqual(actions[0].Name, 'Description')


class TestAction(BaseTeamSupportServiceCase):
    def test_initialisation_with_ids(self):
        self.response.content = """<Action>
                <ID>ActionID</ID>
                <TicketID>ID</TicketID>
                <Name>Description</Name>
            </Action>"""

        action = Action(self.client, ticket_id='ID', action_id='ActionID')
        self.assertEqual(action.ticket_id, 'ID')
        self.assertEqual(action.id, 'ActionID')

    def test_initialisation_with_data(self):
        action_element = etree.fromstring(
            """<Action>
                <ID>ActionID</ID>
                <TicketID>ID</TicketID>
                <Name>Description</Name>
            </Action>""")
        action = Action(self.client, data=action_element)
        self.assertEqual(action.ticket_id, 'ID')
        self.assertEqual(action.id, 'ActionID')

    def test_initialisation_fails_when_missing_args(self):
        self.assertRaises(TypeError, Action, self.client)
        self.assertRaises(TypeError, Action, self.client, ticket_id='ID')
        self.assertRaises(TypeError, Action, self.client, action_id='ActionID')


if __name__ == '__main__':
    unittest.main()
