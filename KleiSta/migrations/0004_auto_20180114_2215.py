# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0003_auto_20180114_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchproduct',
            name='TotalP',
        ),
        migrations.AddField(
            model_name='groupproduct',
            name='BatchId',
            field=models.ForeignKey(default=1, to='KleiSta.Batch'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2018-01-14 22:15'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2018-01-14 22:15'),
        ),
    ]
