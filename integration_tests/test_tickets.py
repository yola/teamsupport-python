#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
integration_tests.test_tickets
----------------------------------

Integration tests for the client
"""
import unittest

from integration_tests import config
from teamsupport import TeamSupportService
from teamsupport.models import Ticket


class TestCreateTicket(unittest.TestCase):
    first_name = 'Eugene Koval'
    email = 'test@email.com'
    ticket_category = 'category'
    ticket_name = 'test ticket dont touch'
    ticket_text = 'test descr dont touch'

    def setUp(self):
        self.client = TeamSupportService(config.ORG_ID, config.AUTH_KEY)
        self.ticket = Ticket.create(
            self.first_name, self.email, self.ticket_category,
            self.ticket_name, self.ticket_text)
        self.contacts = self.client.search_contacts(Email=self.email)
        self.contact_id = self.contacts[0].find('ContactID').text

    def test_ticket_is_created(self):
        self.assertEqual(self.ticket.Name, self.ticket_name)
        self.assertEqual(self.ticket.Formcategory, self.ticket_category)

    def test_ticket_description_is_set(self):
        description = self.client.get_ticket_description(self.ticket.TicketID)
        self.assertEqual(description, self.ticket_text)

    def test_new_contact_is_created(self):
        contacts = self.client.search_contacts(Email=self.email)
        self.assertEqual(len(contacts), 1)

    def tearDown(self):
        self.client.delete_ticket(self.ticket.TicketID)
        self.client.delete_contact(self.contact_id)


class TestCreateTicketForExistingContact(unittest.TestCase):
    first_name = 'Eugene Koval'
    email = 'test@email.com'
    ticket_category = 'category'
    ticket_name = 'test ticket dont touch'
    ticket_text = 'test descr dont touch'

    def setUp(self):
        self.client = TeamSupportService(
            config.ORG_ID, config.AUTH_KEY)

        # Make sure contact with such email doesn't exist.
        self.contacts = self.client.search_contacts(Email=self.email)
        self.assertEqual(len(self.contacts), 0)

        # Create contact manually.
        self.client.create_contact(
            FirstName=self.first_name, EMail=self.email)

        # Create ticket from same email as just created contact.
        self.ticket = Ticket.create(
            self.first_name, self.email, self.ticket_category,
            self.ticket_name, self.ticket_text)

        self.contacts = self.client.search_contacts(Email=self.email)
        self.contact_id = self.contacts[0].find('ContactID').text

    def test_ticket_is_created(self):
        self.assertEqual(self.ticket.Name, self.ticket_name)

    def test_new_contact_is_not_created(self):
        contacts = self.client.search_contacts(Email=self.email)
        self.assertEqual(len(contacts), 1)

    def tearDown(self):
        self.client.delete_ticket(self.ticket.TicketID)
        self.client.delete_contact(self.contact_id)


if __name__ == '__main__':
    unittest.main()
