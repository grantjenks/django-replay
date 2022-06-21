from django.test import Client

from replay.models import Scenario


def test_scenarios(client=None, state=None, **kwargs):
    if client is None:
        client = Client()
    if state is None:
        state = {}
    scenarios = Scenario.objects.filter(**kwargs).order_by('priority', 'id')
    scenario_ids = scenarios.values_list('id', flat=True)
    for scenario_id in scenario_ids:
        test_scenario(client=client, state=state, pk=scenario_id)


def test_scenario(client=None, state=None, **kwargs):
    if client is None:
        client = Client()
    if state is None:
        state = {}
    scenario = Scenario.objects.get(**kwargs)
    scenario.test(client=client, state=state)
