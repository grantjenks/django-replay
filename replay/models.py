"""Django Replay Models

* Remember to use dumpdata and loaddata!
* Do not make actions into templates/generics without great care! Some data
  like files may be deleted because they are stored outside the database.

"""

import base64
import json
import logging
import re
import string
import uuid

from django.db import models
from django.test import Client

HTTP_METHODS = (
    ('GET', 'GET'),
    ('POST', 'POST'),
)


def expand(text, mapping):
    template = string.Template(text)
    return template.substitute(mapping)


class Scenario(models.Model):
    name = models.TextField(unique=True)
    priority = models.FloatField(
        default=1.0,
        help_text='Scenarios are run in ascending priority.',
    )

    def test(self, client=None, state=None):
        if client is None:
            client = Client()

        if state is None:
            state = {}

        log = logging.getLogger('replay.test')
        log.debug('Scenario: %r', self)
        actions = Action.objects.filter(scenario=self).order_by('order', 'id')
        errors = []

        for action in actions:
            log.debug('Action: %r', action)
            status_code, content = self._request(client, action, state)

            if status_code != action.status_code:
                message = 'FAIL %r status code: %s expected: %s'
                data = action, status_code, action.status_code
                log.error(message, *data)
                errors.append(message % data)
                for key, value in state.items():
                    log.error('FAIL %s = %s', key, value)
                break

            validators = Validator.objects.filter(action=action)
            validators = validators.order_by('order', 'id')

            if validators:
                if isinstance(content, bytes):
                    content = content.decode('utf-8')

            for validator in validators:
                pattern = expand(validator.pattern, state)
                match = re.search(pattern, content)

                if match:
                    log.debug('Validator: %r', validator)
                    state.update(match.groupdict())
                else:
                    log.error('Pattern: %s', pattern)
                    log.error('Content: %s', content)
                    message = 'FAIL %r - %r'
                    data = action, validator
                    log.error(message, *data)
                    errors.append(message % (action, validator))

        if errors:
            raise AssertionError(str(errors))

    @staticmethod
    def _request(self, client, action, state):
        func = getattr(client, action.method.lower())
        uuid_bytes = uuid.uuid4().bytes
        uuid_base64 = base64.urlsafe_b64encode(uuid_bytes)
        uuid_clean = uuid_base64.strip(b'=').decode()
        state['__uuid'] = uuid_clean
        data = json.loads(expand(action.data, state))
        files = json.loads(expand(action.files, state))
        path = expand(action.path, state)
        for key, value in files.items():
            data[key] = open(value, 'rb')
        response = func(path, data)
        status_code = str(response.status_code)
        redirect = '300' <= status_code < '400'
        content = response.url if redirect else response.content
        return status_code, content

    def __str__(self):
        return self.name


class Action(models.Model):
    scenario = models.ForeignKey(
        Scenario,
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    order = models.FloatField(
        default=1.0,
        help_text='Actions are run in ascending order.',
    )
    name = models.TextField(blank=True, default='')
    method = models.CharField(max_length=8, choices=HTTP_METHODS)
    path = models.TextField()
    data = models.TextField(
        help_text='HTTP parameters in JSON format. Supports string templating.'
        ' Example: $name or $(name).',
    )
    files = models.TextField(
        help_text='Uploaded files in JSON format. Key and value pairs'
        ' correspond to filename and file-path pairs. Supports string'
        ' templating. Example: $name and $(name).',
    )
    status_code = models.CharField(max_length=3)
    content = models.TextField(blank=True)

    def __str__(self):
        fields = (self.id, self.method, self.path)
        value = self.name or '<Action: %s %s %s>' % fields
        return value[:68]


class Validator(models.Model):
    action = models.ForeignKey(
        Action,
        related_name='validators',
        on_delete=models.CASCADE,
    )
    order = models.FloatField(
        default=1.0,
        help_text='Validators are run in ascending order.',
    )
    pattern = models.TextField(
        help_text='Matched against HTTP response. Supports regular'
        ' expressions. Symbolic group names are stored and may be'
        ' used for string templating. Example: (?P&lt;name&gt;pattern)',
    )

    def __str__(self):
        return self.pattern[:68]
