Python TeamSupport Client
=========================


|Build Status| |Latest Version|

Python library for interfacing with the TeamSupport XML API, using `demands <https://github.com/yola/demands>`__.

Free software: MIT license

Features
--------

-  Client methods parse response content in order to return LXML Element
   objects
-  Converting Python dictionaries into XML for POST and PUT calls
-  Simple models for Tickets and Actions.

Usage
-----

::

    from teamsupport import Ticket, init

    init(<org_id>, <auth_key>[, default_ticket_type=<>, default_ticket_status=<>])

    # Get ticket with given ID/Number.
    ticket = Ticket(<ticket_number_or_ticket_id>)

    # Create new ticket.
    ticket = Ticket.create(
        contact_email, contact_first_name, contact_last_name,
        ticket_name, ticket_text)

    # Get Ticket description.
    descr = ticket.get_description()

    # Update ticket description.
    ticket.set_decription('New description')

    To run integration tests please set correct values in `teamsupport/config.py`
    and run: `nosetests integration_tests`

.. |Build Status| image:: https://img.shields.io/travis/yola/teamsupport-python.svg?style=flat-square
   :target: https://travis-ci.org/yola/teamsupport-python
.. |Latest Version| image:: https://img.shields.io/pypi/v/teamsupport.svg?style=flat-square
   :target: https://warehouse.python.org/project/teamsupport


Running Tests
-------------

Set correct data in teamsupport/config.py

::

    nosetests
