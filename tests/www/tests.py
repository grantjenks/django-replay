import pathlib

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from replay.utils import test_scenarios

pytestmark = pytest.mark.django_db


class ReplayTestCase(TestCase):
    fixtures = [pathlib.Path(__file__).parent.parent / 'replay.json']

    def test_scenarios(self):
        User.objects.create_superuser(username='admin', password='password')
        test_scenarios()
