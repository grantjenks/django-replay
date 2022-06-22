Django Replay
=============

`Django Replay <http://www.grantjenks.com/docs/django-replay/>`__ is an Apache2
licensed Django application that records and replays web requests.


Features
--------

- Record requests/responses as easy as "runserver"
- Test scenarios by replaying requests with validators
- Template requests/responses for dynamic identifiers
- Tested on Python 3.7, 3.8, 3.9, 3.10
- Tested on Django 3.2 LTS and Django 4.0

.. image:: https://github.com/grantjenks/django-replay/workflows/integration/badge.svg
   :target: https://github.com/grantjenks/django-replay/actions?query=workflow%3Aintegration

.. image:: https://github.com/grantjenks/django-replay/workflows/release/badge.svg
   :target: https://github.com/grantjenks/django-replay/actions?query=workflow%3Arelease


Quickstart
----------

Installing Django Replay is simple with `pip
<http://www.pip-installer.org/>`_::

    $ pip install django-replay

Add `replay` to the `INSTALLED_APPS` in `settings.py` like:

.. code::

   INSTALLED_APPS += ['replay']

Then migrate the database like:

.. code::

   $ python manage.py migrate

Django Replay provides two management commands:

1. replayrecord -- like "runserver" but request/responses are recorded.

2. replaytest -- runs the scenarios with actions and validators.

Django Replay also provides three models:

1. Scenario -- ordered list of actions.

2. Action -- recorded request/response template.

3. Validator -- regular expression for response validation.

These models can be edited in the admin.


Tutorial
--------

To get started, follow the Quickstart and then record some actions:

.. code::

   $ python manage.py replayrecord

Navigate to http://127.0.0.1:8000/ and use the web app as normal. Once the
actions are recorded run CTRL-C to stop the command.

Now create some scenarios in the admin:

.. code::

   $ python manage.py runserver

TODO: Insert screenshots of creating scenarios.

The scenarios can be tested manually using:

.. code::

   $ python manage.py replaytest

Remember to clear the content of the actions. Now the tests can be saved in a
fixture.

.. code::

   $ python manage.py dumpdata --indent 4 replay > replay.json

And the scenarios can be integrated with Django's test framework like so:

.. code::

   from django.test import TestCase
   from replay.utils import test_scenarios

    class ReplayTestCase(TestCase):
        fixtures = ['path/to/replay.json']

        def test_scenarios(self):
            test_scenarios()


Templates and Validators
........................

TODO: Describe templating syntax for requests

TODO: Describe regular expression features for validators


Roadmap
-------

- Add details to docs (look for TODO)
- Add more tests ... coverage up to 90% or so
- Support https://pypi.org/project/parse/ in validators
- Support testing management commands
- Support testing emails


Reference and Indices
---------------------

* `Django Replay Documentation`_
* `Django Replay at PyPI`_
* `Django Replay at GitHub`_
* `Django Replay Issue Tracker`_

.. _`Django Replay Documentation`: http://www.grantjenks.com/docs/django-replay/
.. _`Django Replay at PyPI`: https://pypi.python.org/pypi/django-replay/
.. _`Django Replay at GitHub`: https://github.com/grantjenks/django-replay
.. _`Django Replay Issue Tracker`: https://github.com/grantjenks/django-replay/issues


Django Replay License
---------------------

Copyright 2017-2022 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
