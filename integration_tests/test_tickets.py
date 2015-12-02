"""
integration_tests.test_tickets
----------------------------------

Integration tests for the client
"""
from datetime import datetime
import unittest
import uuid

from teamsupport.models import Contact, Ticket


class TestTicket(unittest.TestCase):
    first_name = 'Eugene'
    last_name = 'Koval'
    email = 'test@email.com'
    ticket_name = 'test ticket dont touch'
    ticket_text = 'test descr dont touch'

    @property
    def random_name(self):
        return uuid.uuid4().hex


class TestCreateTicket(TestTicket):
    def setUp(self):
        self.returned_ticket = Ticket.create(
            self.email, self.first_name, self.last_name,
            self.ticket_name, self.ticket_text)
        self.ticket = Ticket(self.returned_ticket.id)
        self.contact = Contact.get(self.email)

    def test_ticket_is_created(self):
        self.assertEqual(self.ticket.Name, self.ticket_name)

    def test_ticket_description_is_set(self):
        description = self.ticket.get_description()
        self.assertEqual(description, self.ticket_text)

    def test_new_contact_is_created(self):
        self.assertEqual(self.contact.FirstName, self.first_name)
        self.assertEqual(self.contact.LastName, self.last_name)
        self.assertEqual(self.contact.Email, self.email)

    def test_ticket_associated_with_contact(self):
        self.assertEqual(len(self.ticket.contacts), 1)
        contact = self.ticket.contacts[0]
        self.assertEqual(contact.FirstName, self.first_name)
        self.assertEqual(contact.Email, self.email)

    def test_created_ticket_is_returned(self):
        self.assertEqual(self.returned_ticket.id, self.ticket.id)
        self.assertEqual(self.returned_ticket.Name, self.ticket.Name)

    def test_datetimes_are_converted_to_datetime_type(self):
        self.assertIsInstance(self.returned_ticket.DateCreated, datetime)
        self.assertIsInstance(self.returned_ticket.DateModified, datetime)

    def tearDown(self):
        self.ticket.delete()
        self.contact.delete()


class TestCreateTicketForExistingContact(TestTicket):
    def setUp(self):
        # Make sure contact with such email doesn't exist.
        contact = Contact.get(self.email)
        self.assertIsNone(contact)

        # Create contact manually.
        self.contact = Contact.create(
            self.email, FirstName=self.first_name, LastName=self.last_name)

        # Create ticket from same email as just created contact.
        self.ticket = Ticket.create(
            self.email, self.first_name, self.last_name,
            self.ticket_name, self.ticket_text)

        self.ticket_contact = Contact.get(self.email)

    def test_ticket_is_created(self):
        self.assertEqual(self.ticket.Name, self.ticket_name)

    def test_new_contact_is_not_created(self):
        self.assertEqual(self.contact.id, self.ticket_contact.id)

    def tearDown(self):
        self.ticket.delete()
        self.contact.delete()


class TestSearchTickets(TestTicket):
    def setUp(self):
        self.created_ticket_name = self.random_name
        self.ticket = Ticket.create(
            self.email, self.first_name, self.last_name,
            self.created_ticket_name, self.ticket_text)
        self.found_tickets = Ticket.search(Name=self.created_ticket_name)

    def test_created_ticket_found(self):
        self.assertEqual(len(self.found_tickets), 1)
        self.assertEqual(self.found_tickets[0].Name, self.created_ticket_name)

    def tearDown(self):
        ticket_contacts = self.ticket.contacts
        [t.delete() for t in self.found_tickets]
        [c.delete() for c in ticket_contacts]


class TestDeleteTicket(TestTicket):
    def setUp(self):
        self.created_ticket_name = self.random_name
        self.ticket = Ticket.create(
            self.email, self.first_name, self.last_name,
            self.created_ticket_name, self.ticket_text)
        self.assertEqual(len(Ticket.search(Name=self.created_ticket_name)), 1)

        self.contacts = self.ticket.contacts
        self.ticket.delete()
        self.found_tickets = Ticket.search(Name=self.created_ticket_name)

    def test_ticket_is_deleted(self):
        self.assertEqual(self.found_tickets, [])

    def tearDown(self):
        [c.delete() for c in self.contacts]


class TestUpdateTicket(TestTicket):
    NEW_NAME = 'new name'

    def setUp(self):
        self.created_ticket_name = self.random_name
        self.ticket = Ticket.create(
            self.email, self.first_name, self.last_name,
            self.created_ticket_name, self.ticket_text)
        self.ticket.update(Name=self.NEW_NAME)
        self.ticket = Ticket(self.ticket.id)

    def test_ticket_name_is_updated(self):
        self.assertEqual(self.ticket.Name, self.NEW_NAME)

    def tearDown(self):
        contacts = self.ticket.contacts
        self.ticket.delete()
        [c.delete() for c in contacts]
