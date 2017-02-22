# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replay', '0004_auto_20170217_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validator',
            name='action',
            field=models.ForeignKey(related_name='validators', to='replay.Action'),
            preserve_default=True,
        ),
    ]
