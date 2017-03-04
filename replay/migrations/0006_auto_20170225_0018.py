# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replay', '0005_auto_20170222_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='data',
            field=models.TextField(help_text=b'HTTP parameters in JSON format. Supports string templating. Example: $name or $(name).'),
        ),
        migrations.AlterField(
            model_name='action',
            name='files',
            field=models.TextField(help_text=b'Uploaded files in JSON format. Key and value pairs correspond to filename and file-path pairs. Supports string templating. Example: $name and $(name).'),
        ),
        migrations.AlterField(
            model_name='action',
            name='order',
            field=models.FloatField(default=1.0, help_text=b'Actions are run in ascending order.'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='priority',
            field=models.FloatField(default=1.0, help_text=b'Scenarios are run in ascending priority.'),
        ),
        migrations.AlterField(
            model_name='validator',
            name='order',
            field=models.FloatField(default=1.0, help_text=b'Validators are run in ascending order.'),
        ),
        migrations.AlterField(
            model_name='validator',
            name='pattern',
            field=models.TextField(help_text=b'Matched against HTTP response. Supports regular expressions. Symbolic group names are stored and may be used for string templating. Example: (?P&lt;name&gt;pattern)'),
        ),
    ]
