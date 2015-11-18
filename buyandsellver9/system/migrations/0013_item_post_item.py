# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_comment_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='post_item',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
