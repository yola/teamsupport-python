from property_caching import cached_property


class Ticket(object):
    _data = None

    def __init__(self, client, ticket_id=None, data=None):
        self.client = client
        if data is not None:
            self._data = data
            self.id = data.find('TicketID').text
        elif ticket_id:
            self.id = ticket_id
        elif not (ticket_id or data):
            raise TypeError(
                "__init__() needs either a 'ticket_id' or 'data' argument "
                "(neither given)")

    def __getattr__(self, name):
        if self.data.find(name) is not None:
            return self.data.find(name)
        raise AttributeError(name)

    @property
    def data(self):
        if self._data is None:
            self._data = self.client.get_ticket(self.id)
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
    data = None

    def __init__(self, client, ticket_id=None, action_id=None, data=None):
        self.client = client
        if data is not None:
            self._data = data
            self.ticket_id = data.find('TicketID').text
            self.id = data.find('ID').text
        elif action_id and ticket_id:
            self.ticket_id = ticket_id
            self.id = action_id
        elif not (ticket_id and action_id) and not data:
            raise TypeError(
                "__init__() needs either both a 'ticket_id' and 'action_id' "
                "or a 'data' argument (neither given)")

    def __getattr__(self, name):
        if self.data.find(name) is not None:
            return self.data.find(name)
        raise AttributeError(name)

    @property
    def data(self):
        if self._data is None:
            self._data = self.client.get_ticket_action(self.ticket_id, self.id)
        return self._data
