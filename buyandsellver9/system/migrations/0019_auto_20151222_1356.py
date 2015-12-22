# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0018_auto_20151222_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_rank', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='ranking_id',
            field=models.ForeignKey(blank=True, to='system.Ranking', null=True),
        ),
    ]
