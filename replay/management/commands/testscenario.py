"""Test Scenario Management Command

"""

import json
import re
import string
import urlparse

from django.core.management.base import BaseCommand, CommandError
from django.test import Client

from replay.models import Validator, Scenario, Step

def expand(text, mapping):
    template = string.Template(text)
    return template.substitute(mapping)


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        try:
            scenarios = []
            for name in args:
                scenario = Scenario.objects.get(name=name)
                scenarios.append(scenario)
        except Scenario.DoesNotExist:
            message = 'scenario with name %r does not exist' % name
            raise CommandError(message)
        else:
            if not scenarios:
                scenarios = Scenario.objects.all().order_by('priority', 'id')

        self.client = Client()
        state = {}

        for scenario in scenarios:
            self.run(scenario, state)


    def run(self, scenario, state):
        steps = Step.objects.filter(scenario=scenario).order_by('order', 'id')
        errors = 0

        for step in steps:
            action = step.action
            status_code, content = self.request(action, state)
            
            if status_code != action.status_code:
                message = 'FAIL %r status code: %s expected: %s'
                data = action, status_code, action.status_code
                self.stdout.write(message % data)
                self.stdout.write('FAIL STATE')
                for key, value in state.items():
                    self.stdout.write('FAIL %s = %s' % (key, value))
                
                errors += 1
                break

            validators = Validator.objects.filter(action=action)
            validators = validators.order_by('order', 'id')
            
            for validator in validators:
                pattern = expand(validator.pattern, state)
                match = re.search(pattern, content)

                if match:
                    message = 'PASS %r %r %r' % (scenario, action, validator)
                    self.stdout.write(message)
                    state.update(match.groupdict())
                else:
                    message = 'FAIL %r %r %r' % (scenario, action, validator)
                    self.stdout.write(message)
                    errors += 1

        if errors:
            raise CommandError('%s errors' % errors)


    def request(self, action, state):
        func = getattr(self.client, action.method.lower())
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
