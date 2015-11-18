# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0014_auto_20151105_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='item',
            name='post_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
