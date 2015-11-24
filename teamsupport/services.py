# -*- coding: utf-8 -*-

from __future__ import absolute_import

from demands import HTTPServiceClient
from lxml import etree

from teamsupport import config
from teamsupport.utils import to_xml


class XMLHTTPServiceClient(HTTPServiceClient):
    def _format_xml_request(self, request_params):
        data_set = request_params.get('data') is not None
        if request_params.get('send_as_xml') and data_set:
            data = request_params['data']
            if isinstance(data, dict):
                data = to_xml(request_params['root'], data)
            request_params['data'] = etree.tostring(
                data, encoding='utf-8', xml_declaration=True,
                pretty_print=True)
            request_params.setdefault('headers', {})
            request_params['headers']['Content-Type'] = 'application/xml'
        return request_params

    def pre_send(self, request_params):
        """Override this method to modify sent request parameters"""
        request_params = super(XMLHTTPServiceClient, self).pre_send(
            request_params)
        return self._format_xml_request(request_params)

    def parse_xml_response(self, response):
        return etree.fromstring(response.content)


class TeamSupportService(XMLHTTPServiceClient):
    def __init__(self, **kwargs):
        if config.ORG_ID is None or config.AUTH_KEY is None:
            raise RuntimeError(
                'You need to call init(<org_id>, <auth_key>) first.'
                ' To run integration tests edit config.py manually')

        super(TeamSupportService, self).__init__(
            url='https://app.teamsupport.com/api/xml/',
            auth=(config.ORG_ID, config.AUTH_KEY), **kwargs)

    def search_tickets(self, **query_params):
        response = self.get('tickets/', params=query_params)
        content = self.parse_xml_response(response)
        return content

    def search_contacts(self, **query_params):
        response = self.get('contacts/', params=query_params)
        return self.parse_xml_response(response)

    def create_contact(self, data):
        response = self.post(
            'contacts/', root='Contact', data=data, send_as_xml=True)
        return self.parse_xml_response(response)

    def get_contact(self, contact_id):
        response = self.get('contacts/{0}'.format(contact_id))
        return self.parse_xml_response(response)

    def delete_contact(self, contact_id):
        self.delete('contacts/{}'.format(contact_id))

    def create_ticket(self, data):
        response = self.post(
            'tickets', root='Ticket', data=data, send_as_xml=True)
        return self.parse_xml_response(response)

    def get_ticket(self, ticket_id):
        response = self.get('Tickets/{0}'.format(ticket_id))
        return self.parse_xml_response(response)

    def delete_ticket(self, ticket_id):
        self.delete('tickets/{0}'.format(ticket_id))

    def update_ticket(self, ticket_id, data):
        response = self.put(
            'tickets/{0}'.format(ticket_id),
            data=data, root='Ticket', send_as_xml=True)
        return self.parse_xml_response(response)

    def get_ticket_actions(self, ticket_id, **query_params):
        response = self.get(
            'tickets/{0}/Actions'.format(ticket_id), params=query_params)
        return self.parse_xml_response(response)

    def get_ticket_contacts(self, ticket_id):
        response = self.get('tickets/{0}/Contacts'.format(ticket_id))
        return self.parse_xml_response(response)

    def get_ticket_customers(self, ticket_id):
        response = self.get('tickets/{0}/Customers'.format(ticket_id))
        return self.parse_xml_response(response)

    def get_ticket_action(self, ticket_id, action_id):
        response = self.get(
            'tickets/{0}/Actions/{1}'.format(ticket_id, action_id))
        return self.parse_xml_response(response)

    def get_ticket_statuses(self):
        response = self.get('properties/ticketstatuses/')
        return self.parse_xml_response(response)

    def get_ticket_types(self):
        response = self.get('properties/tickettypes/')
        return self.parse_xml_response(response)

    def update_ticket_action(self, ticket_id, action_id, data):
        response = self.put(
            'tickets/{0}/Actions/{1}'.format(ticket_id, action_id),
            root='Action', data=data, send_as_xml=True)
        return self.parse_xml_response(response)

    def get_user(self, user_id):
        response = self.get('users/{0}'.format(user_id))
        return self.parse_xml_response(response)

    def get_users(self, **query_params):
        response = self.get('users/', params=query_params)
        content = self.parse_xml_response(response)
        return content

    def get_customer_contacts(self, customer_id):
        response = self.get('tickets/{0}/Customers'.format(customer_id))
        return self.parse_xml_response(response)
