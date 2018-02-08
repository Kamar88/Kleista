# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0005_auto_20180117_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupproduct',
            name='SampleNo',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2018-02-05 23:10'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2018-02-05 23:10'),
        ),
    ]
