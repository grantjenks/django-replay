"""Test Scenario Management Command
"""

from django.core.management.base import BaseCommand

from ...utils import test_scenario, test_scenarios


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('scenario', nargs='*')

    def handle(self, *args, **options):
        names = options['scenario']
        if names:
            for name in names:
                test_scenario(name=name)
        else:
            test_scenarios()
