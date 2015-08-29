from property_caching import cached_property



class Ticket(object):
    def __init__(self, client, ticket_id=None, data=None):
        self.client = client
        self._data = data
        if ticket_id:
            self._data = self.client.get_ticket(ticket_id)
        elif not (ticket_id or data):
            raise TypeError(
                "__init__() needs either a 'ticket_id' or 'data' argument "
                "(neither given)")
        self.id = self.TicketID

    def __getattr__(self, name):
        if self.data.find(name) is not None:
            return self.data.find(name).text
        raise AttributeError(name)

    @property
    def data(self):
        return self._data

    @cached_property
    def actions(self):
        actions = self.client.get_ticket_actions(self.id)
        return [
            Action(
                client=self.client, data=action
            ) for action in actions.findall('Action')
        ]


class Action(object):
    def __init__(self, client, ticket_id=None, action_id=None, data=None):
        self.client = client
        self._data = data
        if action_id and ticket_id:
            self._data = self.client.get_ticket_action(ticket_id, action_id)
        elif not (ticket_id and action_id) and not data:
            raise TypeError(
                "__init__() needs either both a 'ticket_id' and 'action_id' "
                "or a 'data' argument (neither given)")
        self.ticket_id = self.TicketID
        self.id = self.ID

    def __getattr__(self, name):
        if self.data.find(name) is not None:
            return self.data.find(name).text
        raise AttributeError(name)

    @property
    def data(self):
        return self._data
