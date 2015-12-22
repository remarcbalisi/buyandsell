# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_auto_20151128_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_update', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='update_rank',
            field=models.ForeignKey(blank=True, to='system.Ranking', null=True),
        ),
    ]
