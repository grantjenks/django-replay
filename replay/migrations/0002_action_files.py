# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='files',
            field=models.TextField(default='{}'),
            preserve_default=False,
        ),
    ]
