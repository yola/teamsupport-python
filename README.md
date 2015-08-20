# Python TeamSupport Client

[![](https://img.shields.io/travis/yola/teamsupport-python.svg?style=flat-square)](https://travis-ci.org/yola/teamsupport-python)
[![](https://img.shields.io/pypi/v/teamsupport-python?style=flat-square)](https://warehouse.python.org/project/teamsupport-python)


Python library for interfacing with the TeamSupport XML API, using
[demands](https://github.com/yola/demands).

* Free software: MIT license
* Documentation: https://teamsupport-python.readthedocs.org.

## Features

* Client methods parse response content in order to return LXML Element objects
* Converting Python dictionaries into XML for POST and PUT calls

## Usage

```
client = TeamSupportService(TEAMSUPPORT_ORG_ID, TEAMSUPPORT_AUTH_KEY)

# Fetch all tickets without custom fields
tickets = client.get_tickets()

# Update description of a ticket
client.update_ticket_action(
    ticket_id, action_id, data={'Description': 'New description'})
```
