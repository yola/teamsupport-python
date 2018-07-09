from dateutil.parser import parse
from property_caching import cached_property
from querylist import QueryList

from teamsupport import config
from teamsupport.services import TeamSupportService
from teamsupport.errors import MissingArgumentError


def _find_dict_matching_items(list_of_dicts, **kwargs):
    for dct in list_of_dicts:
        for (key, value) in kwargs.items():
            if dct.get(key) != value:
                break
        else:
            return dct


class TSModel(object):
    datetime_fields = ('DateCreated', 'DateModified')

    def __getattr__(self, name):
        value = self.data.get(name)
        if value is None:
            raise AttributeError(name)

        if name in self.datetime_fields:
            value = parse(value)

        return value

    @classmethod
    def get_client(cls):
        return TeamSupportService()

    @cached_property
    def client(self):
        return self.get_client()


class Ticket(TSModel):
    _CACHED_TICKET_STATUSES = None
    _CACHED_TICKET_TYPES = None
    _ACTION_TYPE_DESCRIPTION = 1

    def __init__(self, ticket_id=None, data=None):
        self.data = data
        if ticket_id:
            self.data = self.client.get_ticket(ticket_id)
        elif self.data is None:
            raise MissingArgumentError(
                "__init__() needs either a 'ticket_id' or 'data' argument "
                '(neither given)')

        id_attr = 'ID' if 'ID' in self.data else 'TicketID'
        self.id = self.data[id_attr]

    @classmethod
    def create(cls, user_email, user_first_name, user_last_name, title,
               description, **params):
        # We need to associate ticket with Contact, otherwise ticket doesn't
        # make sense. First, we try to find an existing contact.
        contact = Contact.get(user_email)
        if contact is None:
            # Otherwise - create new one.
            contact = Contact.create(
                user_email, FirstName=user_first_name,
                LastName=user_last_name
            )

        ticket_type_id = cls._get_ticket_type_id(config.DEFAULT_TICKET_TYPE)

        data = {
            'Name': title,
            'ContactID': contact.id,
            'TicketStatusID': cls._get_ticket_status_id(
                ticket_type_id, config.DEFAULT_TICKET_STATUS),
            'TicketTypeID': ticket_type_id,
            'IsVisibleOnPortal': True,
        }
        data.update(params)

        ticket = Ticket(data=cls.get_client().create_ticket(data))
        ticket.set_description(description)
        return ticket

    @classmethod
    def search(cls, **query_params):
        client = cls.get_client()
        return [Ticket(data=data)
                for data in client.search_tickets(**query_params)]

    def update(self, **data):
        self.data = self.client.update_ticket(self.id, data)
        return self

    @classmethod
    def _get_ticket_status_id(cls, ticket_type_id, ticket_status_name):
        statuses = cls._get_ticket_statuses()
        status_dict = _find_dict_matching_items(
            statuses, TicketTypeID=ticket_type_id, Name=ticket_status_name)
        return status_dict['ID'] if status_dict else None

    @classmethod
    def _get_ticket_type_id(cls, ticket_type_name):
        ticket_types = cls._get_ticket_types()
        type_dict = _find_dict_matching_items(
            ticket_types, Name=ticket_type_name)
        return type_dict['ID'] if type_dict else None

    @classmethod
    def _get_ticket_statuses(cls):
        if cls._CACHED_TICKET_STATUSES is not None:
            return cls._CACHED_TICKET_STATUSES

        cls._CACHED_TICKET_STATUSES = cls.get_client().get_ticket_statuses()
        return cls._CACHED_TICKET_STATUSES

    @classmethod
    def _get_ticket_types(cls):
        if cls._CACHED_TICKET_TYPES is not None:
            return cls._CACHED_TICKET_TYPES

        cls._CACHED_TICKET_TYPES = cls.get_client().get_ticket_types()
        return cls._CACHED_TICKET_TYPES

    def delete(self):
        self.client.delete_ticket(self.id)

    def get_description(self):
        ticket_actions = self.client.get_ticket_actions(
            self.id, SystemActionTypeID=self._ACTION_TYPE_DESCRIPTION)
        if ticket_actions is not None:
            return ticket_actions[0]['Description']
        return None

    def set_description(self, description):
        # Description is an Action in TeamSupport API. That action is created
        # automatically when the ticket is created. We need to query it's ID
        # and update this action to set ticket description.
        ticket_actions = self.client.get_ticket_actions(
            self.id, SystemActionTypeID=self._ACTION_TYPE_DESCRIPTION)
        action_id = ticket_actions[0]['ID']
        self.client.update_ticket_action(
            self.id, action_id, {'Description': description})

    @cached_property
    def actions(self):
        actions = self.client.get_ticket_actions(self.id)
        return QueryList(
            [Action(data=action) for action in actions], wrap=False
        )

    @cached_property
    def contacts(self):
        contacts = self.client.get_ticket_contacts(self.id)
        return QueryList(
            [Contact(data=contact) for contact in contacts], wrap=False
        )

    @cached_property
    def customers(self):
        customers = self.client.get_ticket_customers(self.id)
        return QueryList(
            [Customer(data=customer) for customer in customers], wrap=False
        )


class Action(TSModel):
    def __init__(self, ticket_id=None, action_id=None, data=None):
        self.data = data
        if action_id and ticket_id:
            self.data = self.client.get_ticket_action(ticket_id, action_id)
        elif not self.data:
            raise MissingArgumentError(
                "__init__() needs either both a 'ticket_id' and 'action_id' "
                "or a 'data' argument (neither given)")
        self.ticket_id = self.TicketID

        id_attr = 'ID' if 'ID' in self.data else 'ActionID'
        self.id = self.data[id_attr]


class Contact(TSModel):
    def __init__(self, data):
        self.data = data
        id_attr = 'ID' if 'ID' in self.data else 'ContactID'
        self.id = self.data[id_attr]

    @classmethod
    def get(cls, email):
        """Return first contact with given email."""
        client = cls.get_client()
        contacts = client.search_contacts(Email=email)
        if len(contacts) >= 1:
            return Contact(data=contacts[0])
        return None

    @classmethod
    def create(self, email, **data):
        client = self.get_client()
        contact_data = {'Email': email}
        contact_data.update(data)
        contact_data = client.create_contact(contact_data)
        return Contact(data=contact_data)

    def delete(self):
        self.client.delete_contact(self.id)


class Customer(TSModel):
    def __init__(self, data):
        self.data = data
        id_attr = 'ID' if 'ID' in self.data else 'CustomerID'
        self.id = self.data[id_attr]

    @cached_property
    def contacts(self):
        contacts = self.client.get_customer_contacts(self.id)
        return QueryList(
            [Contact(data=contact)
                for contact in contacts.findall('Contact')], wrap=False)
