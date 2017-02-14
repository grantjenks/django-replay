# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(default=b'', blank=True)),
                ('method', models.CharField(max_length=8, choices=[(b'GET', b'GET'), (b'POST', b'POST')])),
                ('path', models.TextField()),
                ('data', models.TextField()),
                ('status_code', models.CharField(max_length=3)),
                ('content', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
                ('priority', models.FloatField(default=1.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.FloatField(default=1.0)),
                ('action', models.ForeignKey(to='replay.Action')),
                ('scenario', models.ForeignKey(to='replay.Scenario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Validator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.FloatField(default=1.0)),
                ('pattern', models.TextField()),
                ('action', models.ForeignKey(to='replay.Action')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
