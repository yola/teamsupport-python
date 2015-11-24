"""
integration_tests.test_tickets
----------------------------------

Integration tests for the client
"""
import unittest

from teamsupport.models import Contact, Ticket


class TestTicket(unittest.TestCase):
    first_name = 'Eugene'
    last_name = 'Koval'
    email = 'test@email.com'
    ticket_name = 'test ticket dont touch'
    ticket_text = 'test descr dont touch'


class TestCreateTicket(TestTicket):
    def setUp(self):
        self.ticket = Ticket.create(
            self.email, self.first_name, self.last_name,
            self.ticket_name, self.ticket_text)
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
