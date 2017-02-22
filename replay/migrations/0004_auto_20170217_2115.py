# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replay', '0003_auto_20170217_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='action',
        ),
        migrations.RemoveField(
            model_name='step',
            name='scenario',
        ),
        migrations.DeleteModel(
            name='Step',
        ),
    ]
