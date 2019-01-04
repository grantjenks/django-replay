# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publish_date', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='essay',
            field=models.ForeignKey(on_delete=models.CASCADE, to='tests.Essay'),
        ),
    ]
