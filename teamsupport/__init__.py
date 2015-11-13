# -*- coding: utf-8 -*-
from __future__ import absolute_import

import teamsupport.config as config
from teamsupport.models import Action, Ticket, User
from teamsupport.services import TeamSupportService

__author__ = 'Yola Engineers'
__email__ = 'engineers@yola.com'
__version__ = '0.1.4'

__all__ = (Action, TeamSupportService, Ticket, User, config)


def init(org_id, auth_key):
    config.ORG_ID = org_id
    config.AUTH_KEY = auth_key
