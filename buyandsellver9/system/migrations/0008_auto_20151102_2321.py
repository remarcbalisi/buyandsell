# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item_id',
            field=models.ForeignKey(blank=True, to='system.Item', null=True),
        ),
    ]
