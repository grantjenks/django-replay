"""Record Management Command

TODO

* Add support for "runserver" options.

"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        from django.conf import settings
        settings.MIDDLEWARE_CLASSES = (
            ('replay.middleware.RecorderMiddleware',)
            + settings.MIDDLEWARE_CLASSES
        )
        call_command('runserver')
