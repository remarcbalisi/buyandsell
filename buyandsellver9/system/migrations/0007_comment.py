# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20151030_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(null=True)),
                ('post_comment', models.DateTimeField(null=True, blank=True)),
                ('item_id', models.ForeignKey(blank=True, to='system.Item', null=True)),
            ],
        ),
    ]
