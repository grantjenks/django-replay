import pathlib

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from replay.models import Action, Validator
from replay.utils import test_scenario as run_scenario
from replay.utils import test_scenarios

pytestmark = pytest.mark.django_db


class ReplayTestCase(TestCase):
    fixtures = [pathlib.Path(__file__).parent.parent / 'replay.json']

    def test_scenarios(self):
        User.objects.create_superuser(username='admin', password='password')
        test_scenarios()

    def test_replaytest(self):
        User.objects.create_superuser(username='admin', password='password')
        call_command('replaytest')

    def test_replaytest_scenario(self):
        User.objects.create_superuser(username='admin', password='password')
        call_command('replaytest', 'Admin Login')

    def test_scenario_fail_status_code(self):
        with self.assertRaises(AssertionError):
            run_scenario(name='Admin Login')

    def test_scenario_fail_validator(self):
        User.objects.create_superuser(username='admin', password='password')
        validator = Validator.objects.get(pk=23)
        validator.pattern = 'foobar'
        validator.save()
        with self.assertRaises(AssertionError):
            run_scenario(name='Admin Login')


class RecordTestCase(TestCase):
    def test_middleware(self):
        modifier = self.modify_settings(
            MIDDLEWARE={
                'prepend': 'replay.middleware.RecorderMiddleware',
            }
        )
        with modifier:
            self.client.get('/')
        (action,) = Action.objects.all()
        self.assertEqual(action.path, '/')
