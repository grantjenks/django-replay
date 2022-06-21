"""Test Scenario Management Command
"""

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from ...utils import test_scenario, test_scenarios


class Command(BaseCommand):
    LOG_LEVELS = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    def add_arguments(self, parser):
        parser.add_argument('scenario', nargs='*')

    def handle(self, *args, **options):
        settings.ALLOWED_HOSTS.append('testserver')
        verbosity = options['verbosity']
        log_level = self.LOG_LEVELS[verbosity]
        logging.basicConfig(
            format='%(asctime)s %(levelname)8s: %(message)s',
            level=log_level,
        )
        names = options['scenario']
        if names:
            for name in names:
                test_scenario(name=name)
        else:
            test_scenarios()
