from property_caching import cached_property
from querylist import QueryList

from teamsupport.errors import MissingArgumentError


class XmlModel(object):
    def __getattr__(self, name):
        if self.data.find(name) is not None:
            return self.data.find(name).text
        raise AttributeError(name)


class Ticket(XmlModel):
    def __init__(self, client, ticket_id=None, data=None):
        self.client = client
        self.data = data
        if ticket_id:
            self.data = self.client.get_ticket(ticket_id)
        elif not self.data:
            raise MissingArgumentError(
                "__init__() needs either a 'ticket_id' or 'data' argument "
                '(neither given)')
        self.id = self.TicketID

    @cached_property
    def actions(self):
        actions = self.client.get_ticket_actions(self.id)
        return QueryList([
            Action(
                client=self.client, data=action
            ) for action in actions.findall('Action')
        ], wrap=False)

    @cached_property
    def user(self):
        return User(client=self.client, user_id=self.UserID)


class Action(XmlModel):
    def __init__(self, client, ticket_id=None, action_id=None, data=None):
        self.client = client
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
