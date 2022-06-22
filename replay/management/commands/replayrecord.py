"""Replay Record Management Command
"""

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        settings.MIDDLEWARE = list(settings.MIDDLEWARE)
        settings.MIDDLEWARE.insert(0, 'replay.middleware.RecorderMiddleware')
        options.pop('skip_checks')
        call_command('runserver', *args, **options)
