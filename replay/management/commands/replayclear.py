"""Replay Clear Management Command
"""

from django.core.management.base import BaseCommand

from replay.models import Action, Scenario


class Command(BaseCommand):
    def handle(self, *args, **options):
        Action.objects.all().delete()
        Scenario.objects.all().delete()
