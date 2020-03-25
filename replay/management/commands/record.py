"""Record Management Command

TODO

* Add support for "runserver" options.

"""

import itertools

from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        # pylint: disable=import-outside-toplevel
        from django.conf import settings
        iterator = itertools.chain(
            ('replay.middleware.RecorderMiddleware',),
            settings.MIDDLEWARE,
        )
        settings.MIDDLEWARE = tuple(iterator)
        call_command('runserver', *args, **options)
