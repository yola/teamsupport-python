Python TeamSupport Client
=========================

|Build Status| |Latest Version|

Python library for interfacing with the TeamSupport XML API, using `demands <https://github.com/yola/demands>`__.

-  Free software: MIT license

Features
--------

-  Client methods parse response content in order to return LXML Element
   objects
-  Converting Python dictionaries into XML for POST and PUT calls
-  Simple models for Tickets and Actions.

Usage
-----

::

    client = TeamSupportService(TEAMSUPPORT_ORG_ID, TEAMSUPPORT_AUTH_KEY)

    # Fetch all tickets without custom fields
    tickets = client.get_tickets()

    # Update description of a ticket
    client.update_ticket_action(
        ticket_id, action_id, data={'Description': 'New description'})

.. |Build Status| image:: https://img.shields.io/travis/yola/teamsupport-python.svg?style=flat-square
   :target: https://travis-ci.org/yola/teamsupport-python
.. |Latest Version| image:: https://img.shields.io/pypi/v/teamsupport-python?style=flat-square
   :target: https://warehouse.python.org/project/teamsupport-python
