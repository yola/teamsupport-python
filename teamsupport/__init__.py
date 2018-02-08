# -*- coding: utf-8 -*-
from __future__ import absolute_import

from teamsupport import config
from teamsupport.models import Action, Ticket
from teamsupport.services import TeamSupportService

__author__ = 'Yola Engineers'
__email__ = 'engineers@yola.com'
__version__ = '0.4.1'

__all__ = (Action, TeamSupportService, Ticket, config)


def init(org_id, auth_key):
    config.ORG_ID = org_id
    config.AUTH_KEY = auth_key
