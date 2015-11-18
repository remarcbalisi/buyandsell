# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0013_item_post_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='post_item',
        ),
        migrations.AddField(
            model_name='item',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 6, 49, 38, 314000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
