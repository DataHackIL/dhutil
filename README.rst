dhutil
######
|PyPI-Status| |PyPI-Versions| |LICENCE|

Python utils for DataHack.

.. code-block:: bash

  ~ dhutil mail confirm_stat
  Emails stas on DataHack 2017 registration:
  432 total users in the system.
  415 users got a confirmation email.

.. contents::

.. section-numbering::


Installation
============

Install ``dhutil`` with:

.. code-block:: bash

  pip install dhutil


Configure
=========

``dhutil`` uses configuration files located at a folder named ``.datahack`` in your home folder (i.e. ``~/.datahack``). Create this folder and populated it with the following mentioned files.


MongoDB
-------

To enable MongoDB access, put a ``mongodb_credentials.json`` file in the ``~/.datahack`` folder with the following properties:

.. code-block:: json

  {
    "host": "ds162883.mlab.com",
    "port": "26552",
    "usr": "some_user",
    "pwd": "pAsswOrd",
    "authSource": "db_name"
  }

These are example values; you need to use the host and port supplied by mlab, a username and password of a user created inside that mlab database (not the username and password used to log in to mlab!), and the name of that database as the ``authSource`` parameter.


Email
-----

To enable email access, put an ``email_credentials.json`` file in the ``~/.datahack`` folder with the following properties:

.. code-block:: json

  {
      "host": "smtp.zoho.com",
      "port": "587",
      "usr": "zoho_username",
      "pwd": "wOwPassWord"
  }

These are example values; host and port are correct (for the ZohoMail SMTP server), but you need to put the username and password of the ZohoMail account you want to use to send emails, or put in the details of another SMTP server.


Use
===

When you install ``dhutil`` a command (of the corresponding name) giving access to its CLI is installed in you system. Type ``dhutil`` in terminal to get a list of the available sub-commands:

.. code-block:: bash

  ~ dhutil
  Usage: dhutil [OPTIONS] COMMAND [ARGS]...

  A command-line interface for dhutil.

Options:
  --help  Show this message and exit.

Commands:
  mail  Email related commands.


mail
----

Some email-related utilities. Type ``dhutil mail`` in terminal to get a list of the available email-related commands:

.. code-block:: bash

  ~ dhutil mail
  Usage: dhutil mail [OPTIONS] COMMAND [ARGS]...

    Email related commands.

  Options:
    --help  Show this message and exit.

  Commands:
    confirm_send  Send confirmation emails.
    confirm_stat  Status of confirmation emails.


confirm_stat
~~~~~~~~~~~~

The ``dhutil mail confirm_stat`` terminal command will print to termintal status regarding how many user got confirmation (not acceptance email):

.. code-block:: bash

  ~ dhutil mail confirm_stat
  Emails stas on DataHack 2017 registration:
  432 total users in the system.
  415 users got a confirmation email.


confirm_send
~~~~~~~~~~~~

The ``dhutil mail confirm_send`` terminal command will first print to terminal confirmation emails stats, and then send confirmation emails (not acceptance emails) to any registered user who has not gotten one yet, and will mark them as such. Emails are sent with 50 recipents per-email (to no use up the daily email quota), all BCCed so they can't see who else is CCed:

.. code-block:: bash

  ~ dhutil mail confirm_send
  Emails stas on DataHack 2017 registration:
  250 total users in the system.
  247 users got a confirmation email.
  Sending confirmation emails to all non-confirmed users.
  Sending a confirmation email to the following addresses:
  ['test.tesi@test.com', 'second.example@gmail.com', 'third@gmail.com']
  Email sent successfully
  Users marked as confirmed on MongoDB

  ==========
  1 confirmation emails were sent to 3 users.


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
--------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:DataHackIL/dhutil.git


Install in development mode with test dependencies:

.. code-block:: bash

  cd dhutil
  pip install -e ".[test]"


Running the tests
-----------------

To run the tests (none at the moment), use

.. code-block:: bash

  python -m pytest --cov=dhutil


Adding documentation
--------------------

This project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings (in my personal opinion, of course). When documenting code you add to this project, please follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======
Created by Shay Palachy  (shay.palachy@gmail.com).

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/dhutil.svg
  :target: https://pypi.python.org/pypi/dhutil

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/dhutil.svg
   :target: https://pypi.python.org/pypi/dhutil

.. |LICENCE| image:: https://img.shields.io/pypi/l/dhutil.svg
  :target: https://pypi.python.org/pypi/dhutil
