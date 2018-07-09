# -*- coding: utf-8 -*-
from __future__ import absolute_import

from teamsupport import config
from teamsupport.models import Action, Ticket
from teamsupport.services import TeamSupportService

__author__ = 'Yola Engineers'
__email__ = 'engineers@yola.com'
__version__ = '0.5.0'

__all__ = (Action, TeamSupportService, Ticket, config)


def init(
        org_id, auth_key, default_ticket_type='Support',
        default_ticket_status='New'):
    config.ORG_ID = org_id
    config.AUTH_KEY = auth_key
    config.DEFAULT_TICKET_TYPE = default_ticket_type
    config.DEFAULT_TICKET_STATUS = default_ticket_status
