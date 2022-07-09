from unittest import mock

import pytest
from django.core.management import call_command

from replay.models import Action

pytestmark = pytest.mark.django_db


def test_action():
    action = Action.objects.create(
        name='Test',
        method='GET',
        path='/',
        data='{}',
        files='{}',
        status_code='200',
        content='',
    )
    assert str(action) == 'Test'


def test_record(monkeypatch):
    mock_call_command = mock.Mock()
    monkeypatch.setattr(
        'replay.management.commands.replayrecord.call_command',
        mock_call_command,
    )
    call_command('replayrecord')
    mock_call_command.assert_called()
