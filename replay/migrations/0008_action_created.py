# Generated by Django 2.1.7 on 2021-03-08 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('replay', '0007_auto_20190104_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
