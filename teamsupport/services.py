# -*- coding: utf-8 -*-

from __future__ import absolute_import

from demands import HTTPServiceClient
from lxml import etree

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
    def __init__(self, org_id, auth_token, **kwargs):
        super(TeamSupportService, self).__init__(
            url='https://app.teamsupport.com/api/xml/',
            auth=(org_id, auth_token), **kwargs)
        self.org_id = org_id
        self.auth_token = auth_token

    def search_tickets(self, query_params=None):
        response = self.get('Tickets/', params=query_params)
        content = self.parse_xml_response(response)
        return content

    def search_contacts(self, **query_params):
        response = self.get('Contacts/', params=query_params)
        return self.parse_xml_response(response)

    def create_contact(self, **data):
        response = self.post(
            'Contacts/', root='Contact', data=data, send_as_xml=True)
        return self.parse_xml_response(response)

    def get_contact(self, contact_id):
        response = self.get('Contacts/{0}'.format(contact_id))
        return self.parse_xml_response(response)

    def delete_contact(self, contact_id):
        self.delete('Contacts/{}'.format(contact_id))

    def create_ticket(self, data):
        response = self.post(
            'tickets', root='Ticket', data=data, send_as_xml=True)
        return self.parse_xml_response(response)

    def set_ticket_description(self, ticket_id, description):
        # Description is an Action in TeamSupport API. That action is created
        # automatically when the ticket is created. We need to query it's ID
        # and update this action to set ticket description.
        ticket_actions = self.get_ticket_actions(
            ticket_id, {'SystemActionTypeID': 1})
        action_id = ticket_actions[0].find('ActionID').text
        self.update_ticket_action(
            ticket_id, action_id, {'Description': description})

    def get_ticket_description(self, ticket_id):
        actions = self.get_ticket_actions(
            ticket_id, {'SystemActionTypeID': 1})
        if len(actions) == 1:
            return actions[0].find('Description').text
        else:
            return None

    def get_ticket(self, ticket_id):
        response = self.get('Tickets/{0}'.format(ticket_id))
        return self.parse_xml_response(response)

    def delete_ticket(self, ticket_id):
        self.delete('Tickets/{0}'.format(ticket_id))

    def update_ticket(self, ticket_id, data):
        response = self.put(
            'Tickets/{0}'.format(ticket_id),
            data=data, root='Ticket', send_as_xml=True)
        return self.parse_xml_response(response)

    def get_ticket_actions(self, ticket_id, query_params=None):
        response = self.get(
            'Tickets/{0}/Actions'.format(ticket_id), params=query_params)
        return self.parse_xml_response(response)

    def get_ticket_action(self, ticket_id, action_id):
        response = self.get(
            'Tickets/{0}/Actions/{1}'.format(ticket_id, action_id))
        return self.parse_xml_response(response)

    def update_ticket_action(self, ticket_id, action_id, data):
        response = self.put(
            'Tickets/{0}/Actions/{1}'.format(ticket_id, action_id),
            root='Action', data=data, send_as_xml=True)
        return self.parse_xml_response(response)

    def get_user(self, user_id):
        response = self.get('users/{0}'.format(user_id))
        return self.parse_xml_response(response)

    def get_users(self, **query_params):
        response = self.get('Users/', params=query_params)
        content = self.parse_xml_response(response)
        return content
