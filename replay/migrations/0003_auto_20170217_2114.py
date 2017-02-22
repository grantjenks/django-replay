# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import defaultdict

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Scenario = apps.get_model('replay', 'Scenario')
    Action = apps.get_model('replay', 'Action')
    Step = apps.get_model('replay', 'Step')

    mapping = defaultdict(list)

    for step in Step.objects.using(db_alias).all():
        mapping[step.action_id].append(step)

    for action_id in list(mapping):
        steps = mapping[action_id]

        while len(steps) > 1:
            step = steps.pop()
            step_action = step.action
            action = Action.objects.using(db_alias).create(
                name=step_action.name,
                method=step_action.method,
                path=step_action.path,
                data=step_action.data,
                files=step_action.files,
                status_code=step_action.status_code,
                content=step_action.content,
            )
            step.action = action
            step.save()

    mapping.clear()

    for step in Step.objects.using(db_alias).all():
        mapping[step.action_id].append(step)

    for action_id, (step,) in mapping.items():
        action = step.action
        action.scenario = step.scenario
        action.order = step.order
        action.save()


class Migration(migrations.Migration):

    dependencies = [
        ('replay', '0002_action_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='order',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='scenario',
            field=models.ForeignKey(default=None, blank=True, to='replay.Scenario', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(
            forwards_func,
        ),
    ]
