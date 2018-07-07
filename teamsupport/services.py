# -*- coding: utf-8 -*-

from __future__ import absolute_import

from demands import HTTPServiceClient

from teamsupport import config


class TeamSupportService(HTTPServiceClient):
    def __init__(self, **kwargs):
        if config.ORG_ID is None or config.AUTH_KEY is None:
            raise RuntimeError(
                'You need to call init(<org_id>, <auth_key>) first.'
                ' To run integration tests edit config.py manually')

        super(TeamSupportService, self).__init__(
            url='https://app.teamsupport.com/api/json/',
            auth=(config.ORG_ID, config.AUTH_KEY), **kwargs)

    def search_tickets(self, **query_params):
        return self.get('tickets/', params=query_params).json()['Tickets']

    def search_contacts(self, **query_params):
        return self.get('contacts/', params=query_params).json()['Contacts']

    def create_contact(self, data):
        return self.post(
            'contacts/', json={'Contact': data}).json()['Contact']

    def get_contact(self, contact_id):
        return self.get('contacts/{0}'.format(contact_id)).json()

    def delete_contact(self, contact_id):
        self.delete('contacts/{}'.format(contact_id))

    def create_ticket(self, data):
        return self.post('tickets/', json={'Ticket': data}).json()['Ticket']

    def get_ticket(self, ticket_id):
        return self.get('Tickets/{0}'.format(ticket_id)).json()['Ticket']

    def delete_ticket(self, ticket_id):
        self.delete('tickets/{0}'.format(ticket_id))

    def update_ticket(self, ticket_id, data):
        return self.put('tickets/{0}'.format(
            ticket_id), json={'Contact': data}).json()['Ticket']

    def get_ticket_actions(self, ticket_id, **query_params):
        return self.get(
            'tickets/{0}/Actions'.format(ticket_id),
            params=query_params).json()['Actions']

    def get_ticket_contacts(self, ticket_id):
        return self.get(
            'tickets/{0}/Contacts'.format(ticket_id)).json()['Contacts']

    def get_ticket_customers(self, ticket_id):
        return self.get(
            'tickets/{0}/Customers'.format(ticket_id)).json()['Customers']

    def get_ticket_action(self, ticket_id, action_id):
        return self.get(
            'tickets/{0}/Actions/{1}'.format(
                ticket_id, action_id)).json()['Action']

    def get_ticket_statuses(self):
        return self.get(
            'properties/ticketstatuses/').json()['TicketStatuses']

    def get_ticket_types(self):
        return self.get('properties/tickettypes/').json()['TicketTypes']

    def update_ticket_action(self, ticket_id, action_id, data):
        return self.put(
            'tickets/{0}/Actions/{1}'.format(ticket_id, action_id),
            json={'TicketAction': data}).json()

    def get_user(self, user_id):
        return self.get('users/{0}'.format(user_id)).json()['User']

    def get_users(self, **query_params):
        return self.get('users/', params=query_params).json()['Users']

    def get_customer_contacts(self, customer_id):
        return self.get(
            'tickets/{0}/Customers'.format(customer_id)).json()['Customers']
