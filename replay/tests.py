import pytest

from replay.models import Action

pytestmark = pytest.mark.django_db  # pylint: disable=invalid-name

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
