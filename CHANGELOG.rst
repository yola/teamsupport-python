Changelog
=========

0.5.0 (2018-07-05)
------------------

- Switched to JSON API.
- Set correct ticket status when creating a ticket


0.4.1 (2018-02-08)
------------------

- Convert input data to str when composing XML.

0.4.0 (2016-10-21)
----------------

- Switched to Demands == 4.0.0

0.3.0 (2015-12-01)
------------------

- Automatically convert DateTime fields to datetime type for Ticket model.

0.2.2 (2015-11-27)
------------------

- Add Ticket.search() and Ticket.update() methods.

0.2.1 (2015-11-27)
------------------

- Fix README.rst formatting.

0.2.0 (2015-11-26)
------------------

-  Add `create` class method to the Ticket model; Add `Contact` model;
-  Remove User model.
-  Change models constructors to not require `client` param.

0.1.3 (2015-09-13)
------------------

-  Fix bug in `update_ticket` method

0.1.2 (2015-09-12)
------------------

-  Bump version to fix PyPI upload issue

0.1.1 (2015-09-12)
------------------

-  Add `User` model and `TeamSupportService.get_user` method.

0.1.0 (2015-09-10)
------------------

-  First release on PyPI.
