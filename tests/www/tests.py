from django.test import TestCase
from replay.utils import test_scenarios, test_scenario


class ReplayTestCase(TestCase):
    fixtures = ['replay.json']

    def test_scenarios(self):
        test_scenarios()

    def test_create_essay(self):
        test_scenario(name='Create Essay')
