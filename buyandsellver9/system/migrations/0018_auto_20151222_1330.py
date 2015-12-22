# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_auto_20151222_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='update_rank',
        ),
        migrations.DeleteModel(
            name='Ranking',
        ),
    ]
