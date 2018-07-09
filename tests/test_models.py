#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_models
----------------------------------

Tests for `teamsupport.models` module.
"""
import unittest
from dateutil.parser import parse

from teamsupport.errors import MissingArgumentError
from teamsupport.models import Action, Ticket
from tests import BaseTeamSupportServiceCase


class TestTicket(BaseTeamSupportServiceCase):
    def setUp(self):
        super(TestTicket, self).setUp()
        self.data = {
            'TicketID': 'ID',
            'DateCreated': '2018-01-01 00:00:00',
            'DateModified': '2018-01-01 00:00:00'
        }

    def test_initialisation_with_id(self):
        self.response.json.return_value = {'Ticket': self.data}
        ticket = Ticket('ID')
        self.assertEqual(ticket.id, self.data['TicketID'])
        self.assertEqual(ticket.DateCreated, parse(self.data['DateCreated']))
        self.assertEqual(
            ticket.DateModified, parse(self.data['DateModified']))

    def test_initialisation_with_data(self):
        ticket = Ticket(data=self.data)
        self.assertEqual(ticket.id, self.data['TicketID'])
        self.assertEqual(ticket.DateCreated, parse(self.data['DateCreated']))
        self.assertEqual(
            ticket.DateModified, parse(self.data['DateModified']))

    def test_initialisation_fails_when_missing_args(self):
        self.assertRaises(MissingArgumentError, Ticket)


class TestAction(BaseTeamSupportServiceCase):
    def setUp(self):
        super(TestAction, self).setUp()
        self.action_data = {
            'ID': 'ActionID',
            'TicketID': 'TicketID',
            'Name': 'Name'
        }

    def test_initialisation_with_ids(self):
        self.action_data = {
            'ActionID': 'ActionID',
            'TicketID': 'TicketID',
            'Name': 'Name'
        }
        self.response.json.return_value = {
            'Action': self.action_data}

        action = Action(ticket_id='TicketID', action_id='ActionID')
        self.assertEqual(action.ticket_id, 'TicketID')
        self.assertEqual(action.id, 'ActionID')

    def test_initialisation_with_data(self):
        action = Action(self.client, data=self.action_data)
        self.assertEqual(action.ticket_id, 'TicketID')
        self.assertEqual(action.id, 'ActionID')
        self.assertEqual(action.Name, 'Name')

    def test_initialisation_fails_when_missing_args(self):
        self.assertRaises(MissingArgumentError, Action)
        self.assertRaises(MissingArgumentError, Action, ticket_id='ID')
        self.assertRaises(MissingArgumentError, Action,
                          action_id='ActionID')


if __name__ == '__main__':
    unittest.main()
