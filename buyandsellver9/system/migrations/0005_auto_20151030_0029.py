# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20151030_0027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='user',
            new_name='user_id',
        ),
    ]
