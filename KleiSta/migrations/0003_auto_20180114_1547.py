# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0002_auto_20180107_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchproduct',
            name='TotalP',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2018-01-14 15:47'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2018-01-14 15:47'),
        ),
    ]
