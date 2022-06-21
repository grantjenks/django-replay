from replay.models import Scenario


def test_scenarios(state=None, **kwargs):
    if state is None:
        state = {}
    scenarios = Scenario.objects.filter(**kwargs).order_by('priority', 'id')
    scenario_ids = scenarios.values_list('id', flat=True)
    for scenario_id in scenario_ids:
        test_scenario(state=state, pk=scenario_id)


def test_scenario(state=None, **kwargs):
    if state is None:
        state = {}
    scenario = Scenario.objects.get(**kwargs)
    scenario.test(state)
