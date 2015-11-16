from property_caching import cached_property
from querylist import QueryList

from teamsupport.services import TeamSupportService
from teamsupport.errors import MissingArgumentError


TICKET_STATUS_NEW = '212203'
TICKET_TYPE_SUPPORT = '35731'


class XmlModel(object):
    def __getattr__(self, name):
        if self.data.find(name) is not None:
            return self.data.find(name).text
        raise AttributeError(name)

    @classmethod
    def get_client(cls):
        return TeamSupportService()

    @cached_property
    def client(self):
        return self.get_client()


class Ticket(XmlModel):
    def __init__(self, ticket_id=None, data=None):
        self.data = data
        if ticket_id:
            self.data = self.client.get_ticket(ticket_id)
        elif not self.data:
            raise MissingArgumentError(
                "__init__() needs either a 'ticket_id' or 'data' argument "
                '(neither given)')
        self.id = self.TicketID

    @classmethod
    def create(cls, first_name, email, category, title, description):
        # We need to associate ticket with Contact, otherwise ticket doesn't
        # make sense. First, we try to find an existing contact.
        contact = Contact.get(first_name, email)
        if contact is None:
            # Otherwise - create new one.
            contact = Contact.create(first_name, email)

        data = {
            'Name': name,
            'FormCategory': category,
            'TicketStatusID': TICKET_STATUS_NEW,
            'TicketTypeID': TICKET_TYPE_SUPPORT,
            'ContactID': contact.id
        }

        ticket = Ticket(data=cls.get_client().create_ticket(data))
        ticket.set_description(description)
        return ticket

    def delete(self):
        self.client.delete_ticket(self.id)

    def get_description(self):
        return self.client.get_ticket_description(self.id)

    def set_description(self, description):
        self.client.set_ticket_description(self.id, description)

    @cached_property
    def actions(self):
        actions = self.client.get_ticket_actions(self.id)
        return QueryList(
            [Action(data=action)
                for action in actions.findall('Action')], wrap=False)

    @cached_property
    def user(self):
        return User(client=self.client, user_id=self.UserID)


class Action(XmlModel):
    def __init__(self, ticket_id=None, action_id=None, data=None):
        self.data = data
        if action_id and ticket_id:
            self.data = self.client.get_ticket_action(ticket_id, action_id)
        elif not self.data:
            raise MissingArgumentError(
                "__init__() needs either both a 'ticket_id' and 'action_id' "
                "or a 'data' argument (neither given)")
        self.ticket_id = self.TicketID
        self.id = self.ID


class User(XmlModel):
    def __init__(self, client, user_id=None, data=None):
        self.client = client
        self.data = data
        if user_id:
            self.data = self.client.get_user(user_id)
        elif not self.data:
            raise MissingArgumentError(
                "__init__() needs either a 'user_id' or 'data' argument "
                '(neither given)')
        self.id = self.UserID


class Contact(XmlModel):
    def __init__(self, data):
        self.data = data
        self.id = self.ContactID

    @classmethod
    def get(cls, first_name, email):
        client = cls.get_client()
        contacts = client.search_contacts(FirstName=first_name, Email=email)
        if len(contacts) >= 1:
            return Contact(data=contacts[0])
        return None

    @classmethod
    def create(self, first_name, email):
        client = self.get_client()
        contact_xml = client.create_contact(FirstName=first_name, Email=email)
        return Contact(data=contact_xml)

    def delete(self):
        self.client.delete_contact(self.id)
