# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.CharField(default=datetime.datetime(2015, 11, 5, 6, 32, 48, 949000, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
