#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
integration_tests.test_services
----------------------------------

Integration tests for the client
"""
import unittest

from integration_tests import config
from teamsupport import TeamSupportService


class CleanedUpTicket(object):
    def __init__(self, client, data):
        self.client = client
        self.data = data
        self.id = None

    def __enter__(self):
        ticket = self.client.create_ticket(data=self.data)
        self.id = ticket.find('TicketID').text
        return self.id

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.delete_ticket(self.id)


class TestTeamSupportService(unittest.TestCase):
    def setUp(self):
        self.client = TeamSupportService(
            config.TEAMSUPPORT_ORG_ID, config.TEAMSUPPORT_AUTH_KEY)

    def test_ticket_flow(self):
        with CleanedUpTicket(
                self.client, data={'TicketStatusID': '220075'}) as ticket_id:
            actions = self.client.get_ticket_actions(ticket_id)
            action_id = None
            for action in actions:
                if action.find('Name').text == 'Description':
                    description = action
                    action_id = description.find('ActionID').text
            if action_id is None:
                raise Exception("Action 'Description' not found")
            self.client.update_ticket_action(
                ticket_id, action_id, data={'Description': 'Test description'})

            action = self.client.get_ticket_action(ticket_id, action_id)
            self.assertEqual(
                action.find('Description').text, 'Test description')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
